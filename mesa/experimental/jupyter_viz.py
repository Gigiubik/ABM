import threading

import matplotlib.pyplot as plt
import networkx as nx
import reacton.ipywidgets as widgets
import solara
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

import mesa

# Avoid interactive backend
plt.switch_backend("agg")


@solara.component
def JupyterViz(
    model_class,
    model_params,
    measures=None,
    name="Mesa Model",
    agent_portrayal=None,
    space_drawer="default",
    play_interval=400,
):
    """Initialize a component to visualize a model.
    Args:
        model_class: class of the model to instantiate
        model_params: parameters for initializing the model
        measures: list of callables or data attributes to plot
        name: name for display
        agent_portrayal: options for rendering agents (dictionary)
        space_drawer: method to render the agent space for
            the model; default implementation is :meth:`make_space`;
            simulations with no space to visualize should
            specify `space_drawer=False`
        play_interval: play interval (default: 400)
    """

    current_step, set_current_step = solara.use_state(0)

    solara.Markdown(name)

    # 0. Split model params
    model_params_input, model_params_fixed = split_model_params(model_params)

    # 1. User inputs
    user_inputs = {}
    for name, options in model_params_input.items():
        user_input = solara.use_reactive(options["value"])
        user_inputs[name] = user_input.value
        make_user_input(user_input, name, options)

    # 2. Model
    def make_model():
        return model_class(**user_inputs, **model_params_fixed)

    model = solara.use_memo(make_model, dependencies=list(user_inputs.values()))

    # 3. Buttons
    ModelController(model, play_interval, current_step, set_current_step)

    with solara.GridFixed(columns=2):
        # 4. Space
        if space_drawer == "default":
            # draw with the default implementation
            make_space(model, agent_portrayal)
        elif space_drawer:
            # if specified, draw agent space with an alternate renderer
            space_drawer(model, agent_portrayal)
        # otherwise, do nothing (do not draw space)

        # 5. Plots
        for measure in measures:
            if callable(measure):
                # Is a custom object
                measure(model)
            else:
                make_plot(model, measure)


@solara.component
def ModelController(model, play_interval, current_step, set_current_step):
    playing = solara.use_reactive(False)
    thread = solara.use_reactive(None)

    def on_value_play(change):
        if model.running:
            do_step()
        else:
            playing.value = False

    def do_step():
        model.step()
        set_current_step(model.schedule.steps)

    def do_play():
        model.running = True
        while model.running:
            do_step()

    def threaded_do_play():
        if thread is not None and thread.is_alive():
            return
        thread.value = threading.Thread(target=do_play)
        thread.start()

    def do_pause():
        if (thread is None) or (not thread.is_alive()):
            return
        model.running = False
        thread.join()

    with solara.Row():
        solara.Button(label="Step", color="primary", on_click=do_step)
        # This style is necessary so that the play widget has almost the same
        # height as typical Solara buttons.
        solara.Style(
            """
        .widget-play {
            height: 30px;
        }
        """
        )
        widgets.Play(
            value=0,
            interval=play_interval,
            repeat=True,
            show_repeat=False,
            on_value=on_value_play,
            playing=playing.value,
            on_playing=playing.set,
        )
        solara.Markdown(md_text=f"**Step:** {current_step}")
        # threaded_do_play is not used for now because it
        # doesn't work in Google colab. We use
        # ipywidgets.Play until it is fixed. The threading
        # version is definite a much better implementation,
        # if it works.
        # solara.Button(label="▶", color="primary", on_click=viz.threaded_do_play)
        # solara.Button(label="⏸︎", color="primary", on_click=viz.do_pause)
        # solara.Button(label="Reset", color="primary", on_click=do_reset)


def split_model_params(model_params):
    model_params_input = {}
    model_params_fixed = {}
    for k, v in model_params.items():
        if check_param_is_fixed(v):
            model_params_fixed[k] = v
        else:
            model_params_input[k] = v
    return model_params_input, model_params_fixed


def check_param_is_fixed(param):
    if not isinstance(param, dict):
        return True
    if "type" not in param:
        return True


def make_user_input(user_input, name, options):
    """Initialize a user input for configurable model parameters.
    Currently supports :class:`solara.SliderInt`, :class:`solara.SliderFloat`,
    and :class:`solara.Select`.

    Args:
        user_input: :class:`solara.reactive` object with initial value
        name: field name; used as fallback for label if 'label' is not in options
        options: dictionary with options for the input, including label,
        min and max values, and other fields specific to the input type.
    """
    # label for the input is "label" from options or name
    label = options.get("label", name)
    input_type = options.get("type")
    if input_type == "SliderInt":
        solara.SliderInt(
            label,
            value=user_input,
            min=options.get("min"),
            max=options.get("max"),
            step=options.get("step"),
        )
    elif input_type == "SliderFloat":
        solara.SliderFloat(
            label,
            value=user_input,
            min=options.get("min"),
            max=options.get("max"),
            step=options.get("step"),
        )
    elif input_type == "Select":
        solara.Select(
            label,
            value=options.get("value"),
            values=options.get("values"),
        )
    else:
        raise ValueError(f"{input_type} is not a supported input type")


def make_space(model, agent_portrayal):
    def portray(g):
        x = []
        y = []
        s = []  # size
        c = []  # color
        for i in range(g.width):
            for j in range(g.height):
                content = g._grid[i][j]
                if not content:
                    continue
                if not hasattr(content, "__iter__"):
                    # Is a single grid
                    content = [content]
                for agent in content:
                    data = agent_portrayal(agent)
                    x.append(i)
                    y.append(j)
                    if "size" in data:
                        s.append(data["size"])
                    if "color" in data:
                        c.append(data["color"])
        out = {"x": x, "y": y}
        if len(s) > 0:
            out["s"] = s
        if len(c) > 0:
            out["c"] = c
        return out

    space_fig = Figure()
    space_ax = space_fig.subplots()
    if isinstance(model.grid, mesa.space.NetworkGrid):
        _draw_network_grid(model, space_ax, agent_portrayal)
    else:
        space_ax.scatter(**portray(model.grid))
    space_ax.set_axis_off()
    solara.FigureMatplotlib(space_fig)


def _draw_network_grid(model, space_ax, agent_portrayal):
    graph = model.grid.G
    pos = nx.spring_layout(graph, seed=0)
    nx.draw(
        graph,
        ax=space_ax,
        pos=pos,
        **agent_portrayal(graph),
    )


def make_plot(model, measure):
    fig = Figure()
    ax = fig.subplots()
    df = model.datacollector.get_model_vars_dataframe()
    ax.plot(df.loc[:, measure])
    ax.set_ylabel(measure)
    # Set integer x axis
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    solara.FigureMatplotlib(fig)


def make_text(renderer):
    def function(model):
        solara.Markdown(renderer(model))

    return function
