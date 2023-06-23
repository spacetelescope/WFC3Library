"""
    This script contains functions written for the IMA
    Viewer notebook in the WFC3Library repo.

    Author
    ------
    Mariarosa Marinelli, Dec 2022

    Use
    ---
    The functions in this script are intended to be
    imported, i.e.:

        from ima_tools import make_interactive_plot
"""

from astropy.io import fits
from astroquery.mast import Observations
import imageio.v2 as imageio
from IPython.display import display
from ipywidgets import interact, interactive, Layout
import ipywidgets as widgets
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib.colors import Normalize
import numpy as np
import os
import shutil

# Plotting functions:
def get_data_and_norm_lims(ext, fits_file, pct_limits=(50, 99.5)):
    """
    Helper function to grab the data from a specific
    extension, find the normalization factors from the
    percentage limits either set by the user or from the
    default percentages.

    Parameters
    ----------
    ext : int
        Integer corresponding to the extension of the
        fits file.
    fits_file : fits
        Fits file at hand.
    pct_limits : tuple of float
        Percentage limits as set by user. Default is a
        lower bound of 50% and upper bound of 99.5%.

    Returns
    -------
    data : array
        Array of data from the specified extension.
    limits : tuple of float
        Lower and upper limits, specific to the extension.
    """
    data = fits_file[ext].data
    data_min = np.nanpercentile(data, pct_limits[0])
    data_max = np.nanpercentile(data, pct_limits[1])
    limits = (data_min, data_max)
    return data, limits

def get_indices(fits_file, ext_type):
    """
    Helper function to grab the indices that are
    relevant and match the extension type specified.

    Parameters
    ----------
    fits_file : fits
        Fits file at hand.
    ext_type : str
        Extension type.

    Returns
    -------
    indices : list of int
        List of extensions, ordered by time.
    """
    indices = [i for i, ext in enumerate(fits_file) if ext.name == ext_type]
    indices.reverse()
    return indices

def make_interactive_plot(filepath, ext_type='SCI'):
    """
    Function to make and display an interactive
    plot for a WFC3/IR IMA file.

    Parameters
    ----------
    filepath : str
        String representation of the path to the
        IMA file.
    ext_type : str
        Extension of the IMA fits file that should
        be displayed. Valid inputs are 'SCI', 'ERR',
        and 'DQ'. Default is 'SCI'.

    Returns
    -------
    plot : tuple or None
        If any input is invalid, then ``plot`` is None,
        otherwise, ``plot`` is a tuple of 5 items:
            fig : `matplotlib.figure.Figure`
            ax :  `matplotlib.axes._subplots.AxesSubplot`
            w : `ipywidgets.widgets.interaction.interactive`
                Contains 3 widgets:
                    cmap :
                    ext :
                    lim_slider :
            filepath : str
            ext_type : str
    """
    inputs = verify_input(filepath, ext_type)

    if inputs == None:
        plot = None

    else:
        fits_file = fits.open(inputs[0])
        indices = get_indices(fits_file, inputs[1])
        rootname = fits_file[0].header['ROOTNAME']
        fig, ax = plt.subplots()
        data, limits = get_data_and_norm_lims(indices[0], fits_file)
        img = ax.imshow(data, origin='lower',
                        cmap='viridis_r',
                        norm=Normalize(vmin=limits[0], vmax=limits[1]))
        cb = fig.colorbar(mappable=img, label='electrons', ax=ax)

        cmap, ext, lim_slider = make_plot_widgets(ext_options=indices)

        def update_img(cmap=cmap,
                       ext=ext,
                       lim_slider=lim_slider):
            data, limits = get_data_and_norm_lims(ext, fits_file, lim_slider)
            img.set_data(data)
            img.set_norm(Normalize(vmin=limits[0], vmax=limits[1]))
            img.set_cmap(cmap)

            view_title = f'{rootname}: [{ext_type.upper()},{ext}]'
            ax.set_title(view_title, fontsize=12)
            cb.update_normal(mappable=img)

            fig.canvas.draw_idle()

            return cmap, ext, lim_slider

        w = interactive(update_img,
                        cmap=cmap,
                        ext=ext,
                        lim_slider=lim_slider)

        display(w)

        plot = (fig, ax, w, filepath, ext_type)

        return plot

def make_plot_widgets(ext_options,
                 cmap_value='viridis_r',
                 lim_value=(50.0,99.5),
                 lim_step=0.1):
    """
    Function to generate the widgets to control and
    display the colormap, image extension, and limits
    for normalization.

    Parameters
    ----------
    ext_options : list of int
        List of integers representing the file extensions
        that should be plotted.
    cmap_value : str
        One of the named Matplotlib colormaps. Default
        value is "viridis_r".
    lim_value : tuple of float
        A two-item tuple containing the lower and upper
        percentile limits for scale normalization. Default
        values are 50% (lower) and 99.5% (upper).

    Returns
    -------
    cmap : widgets.widget_selection.Dropdown
    ext : widgets.widget_selection.SelectionSlider
    lim_slider : widgets.widget_float.FloatRangeSlider

    """
    cmap=widgets.Dropdown(options=plt.colormaps(),
                          value=cmap_value,
                          description='Colormap: ',
                          layout=Layout(width='50%'))
    ext=widgets.SelectionSlider(value=ext_options[0],
                            options=ext_options,
                            description='Extension: ',
                            layout=Layout(width='50%'))
    lim_slider=widgets.FloatRangeSlider(min=0, max=100,
                                        value=lim_value,
                                        step=lim_step,
                                        readout_format='.1f',
                                        description='Scaling (%): ',
                                        layout=Layout(width='50%'))
    return cmap, ext, lim_slider


def verify_input(filepath, ext_type):
    """
    Verify file exists and the extension is valid.

    Parameters
    ----------
    filepath : str
        String representation of the path to the
        IMA file.
    ext_type : str
        Extension of the IMA fits file that should
        be displayed. Valid inputs are 'SCI', 'ERR',
        and 'DQ'. Default is 'SCI'.

    Returns
    -------
    inputs : tuple of str or None
        If both the filepath and the extension are
        valid, returns a tuple of format (filepath,
        ext). Otherwise, returns None.
    """
    if os.path.exists(filepath):
        valid_ext = verify_ext(ext_type)
        if valid_ext != None:
            inputs = (filepath, valid_ext)
        else:
            print('Filepath verified, but extension was not valid.')
            inputs = None
    else:
        print('Filepath could not be verified.')
        inputs = None

    return inputs


def verify_ext(ext_type):
    """
    Parameters
    ----------
    ext_type : str
        Extension of the IMA fits file that should
        be displayed. Valid inputs are 'SCI', 'ERR',
        and 'DQ'. Default is 'SCI'.

    Returns
    -------
    valid_ext : str or None
        If entered extension name (or uppercase version)
        is a valid extension, returns the extension name.
        Otherwise, returns None.
    """
    ext_type = ext_type.upper()
    if ext_type in ['SCI', 'DQ', 'ERR']:
        valid_ext = ext_type

    else:
        if ext_type in ['PRIMARY', 'SAMP', 'TIME']:
            message = f'Cannot display data as image for extension type: {ext_type}'
        else:
            message = f'{ext_type} is not a recognized extension for IMA files.'
        print(f'{message}\nPossible extensions for image data are:\n\tSCI\n\tDQ\n\tERR')
        valid_ext = None

    return valid_ext


# output functions
def get_ax_info(ax):
    """
    Grabs the rootname and the x- and y-limits
    from the current ax view

    Parameters
    ----------
    ax : matplotlib.axes._subplots.AxesSubplot

    Returns
    -------
    rootname : str
        Rootname identifier for the current
        observation.

    xlims, ylims : tuples of int

    """
    rootname = ax.get_title().split(':')[0]

    x1, x2 = ax.get_xlim()
    y1, y2 = ax.get_ylim()

    xlims = (int(x1), int(x2))
    ylims = (int(y1), int(y2))

    return rootname, xlims, ylims

def gif_settings_widgets(plot):
    """
    Parameter
    ---------
    plot : tuple
        `plot`` is a tuple of 3 items, defined in
        make_interactive_plot().
            fig : `matplotlib.figure.Figure`
            ax :  `matplotlib.axes._subplots.AxesSubplot`
            w : `ipywidgets.widgets.interaction.interactive`

    Returns
    -------
    loop_settings : tuple
    time_settings : tuple
    save_settings : tuple
    output_settings : tuple
    """


    ax = plot[1]

    loop_settings = set_looping()
    loop_box = widgets.VBox([loop_settings[0],
                             loop_settings[1],
                             loop_settings[2]],
                            layout=Layout(width='50%', height='150px'))

    time_settings = set_timing()
    time_box = widgets.VBox([time_settings[0],
                             time_settings[1]],
                            layout=Layout(width='50%', height='150px'))

    rootname, xlims, ylims = get_ax_info(ax)

    save_settings = set_saving(rootname, xlims, ylims)
    save_box = widgets.VBox([save_settings[0],
                             save_settings[1],
                             save_settings[2]],
                             layout=Layout(width='100%', height='200px'))

    output_settings = set_output()
    output_col = widgets.VBox([output_settings[0], output_settings[1]])
    output_row = widgets.HBox([output_col, output_settings[6]],
                              layout=Layout(width='100%', height='100px'))


    last_row = widgets.HBox([loop_box, time_box])
    display_grid = widgets.VBox([output_row,
                                 output_settings[8],
                                 save_box,
                                 last_row])
    display(display_grid)

    return loop_settings, time_settings, save_settings, output_settings

def make_default_filename(rootname, xlims, ylims):
    """
    Parameters
    ----------
    rootname : str
        Rootname identifier for the current
        observation.

    xlims, ylims : tuples of int

    Returns
    -------
    default_filename : str
        Default filename to suggest to user.
    """

    zoom_dim = f'{xlims[0]}-{xlims[1]}_{ylims[0]}-{ylims[1]}'
    default_filename = f'{rootname}_{zoom_dim}'
    return default_filename

def set_looping():
    """
    Generates widgets to offer the option to loop
    the gif, and returns the settings.

    Returns
    -------
    caption : widgets.widget_string.HTML
    loop : ``widgets.widget_bool.Checkbox``
        Boolean to determine whether or not to loop
        the GIF frames. Default is False.
    iters : ``widgets.widget_int.IntSlider``
        The number of iterations. If ``loop`` is
        False, value and minimum for slider are
        set to 0 and slider is disabled. Otherwise,
        slider is enabled, and default value and slider
        minimum are set to 1.
    """
    line = 'Do you want to loop your frames in the GIF? Maximum possible iterations is 10.'

    caption = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>'+line+' </p>')

    loop = widgets.Checkbox(description='Loop GIF',
                            value=False)
    iters = widgets.IntSlider(description='Iterations: ',
                              min=1, max=10)

    def adjust_iters(loop):
        if loop:
            display(iters)
            iters.disabled = False
            iters.min = 1
        else:
            iters.disabled = True
            iters.min = 0
            iters.value = 0

    out = widgets.interactive_output(adjust_iters, {'loop': loop})

    return caption, loop, iters


def set_output():
    """
    Sets up widget for user to specify their desired output.

    Returns
    -------
    gif : widgets.widget_box.HBox
        Horizontal widget box composed of:
            gif_label : widgets.widget_string.HTML
            gif_choice : widgets.widget_bool.Checkbox
    gif_from : widgets.widget_box.HBox
        Horizontal widget box composed of:
            gif_from_label : widgets.widget_string.HTML
            gif_from_choice : widgets.widget_selection.Dropdown
    out1 : widgets.widget_output.Output
    caption : widgets.widget_string.HTML
    jpg : widgets.widget_bool.Checkbox
    png : widgets.widget_bool.Checkbox
    choose : widgets.widget_box.VBox
        Vertical widget box composed of:
            caption : widgets.widget_string.HTML
            jpg : widgets.widget_bool.Checkbox
            png : widgets.widget_bool.Checkbox
    out2 : widgets.widget_output.Output
    summary : widgets.widget_string.HTML

    """
    gif_label = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>Do you want to create a GIF? </p>')
    gif_choice = widgets.Checkbox(value=False, description='Make GIF')
    gif = widgets.HBox([gif_label, gif_choice])

    gif_from_label = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>Make GIF from: </p>')
    gif_from_choice = widgets.Dropdown(options=['JPG frames', 'PNG frames'],
                                       value=None,
                                       disabled=True)
    gif_from = widgets.HBox([gif_from_label, gif_from_choice])

    caption = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>Do you want to save the individual frames? </p>')

    jpg = widgets.Checkbox(description='Save JPG frames', value=False)
    png = widgets.Checkbox(description='Save PNG frames', value=False)
    choose = widgets.VBox([caption, jpg, png],
                          layout=Layout(width='50%', height='100px'))

    html_tags = ['<style>p{word-wrap: break-word}</style> <p>', ' </p>']
    summary = widgets.HTML(value='', layout=Layout(width='100%', height='100px'))

    def choices_summary(gif_choice, gif_from_choice, jpg, png):
        """
        Parameters
        ----------
        gif_choice : widgets.widget_bool.Checkbox
        gif_from_choice : widgets.widget_selection.Dropdown
        jpg : widgets.widget_bool.Checkbox
        png : widgets.widget_bool.Checkbox
        """

        if not gif_choice:
            if not jpg and not png:
                summary.value = f'{html_tags[0]}Not saving any files.{html_tags[1]}'
            else:
                if jpg and not png:
                    frame_format = 'JPG'
                if png and not jpg:
                    frame_format = 'PNG'
                else:
                    frame_format = 'JPG and PNG'
                summary.value = f'{html_tags[0]}Saving individual frames as {frame_format} files.{html_tags[1]}'

        else:
            if gif_from_choice == None:
                gif_format = '(no format specified, but default is PNG)'
            else:
                gif_format = f'from {gif_from_choice}'

            if not jpg and not png:
                files = '.'
            else:
                if jpg and not png:
                    save_frames = 'JPG'
                if png and not jpg:
                    save_frames = 'PNG'
                if png and jpg:
                    save_frames = 'JPG and PNG'

                files = f', and saving individual frames as {save_frames} files.'
            summary.value = f'{html_tags[0]}Making GIF {gif_format}{files}{html_tags[1]}'

        display(summary)

    def choice_gif(gif_choice):
        """
        Parameter
        ---------
        gif_choice : widgets.widget_bool.Checkbox
        """
        if gif_choice:
            gif_from_choice.disabled = False
            display(gif_from)
        else:
            gif_from_choice.disabled = True
            gif_from_choice.value = None


    out1 = widgets.interactive_output(choice_gif, {'gif_choice': gif_choice})
    out2 = widgets.interactive_output(choices_summary,
                                      {'gif_choice': gif_choice,
                                       'gif_from_choice': gif_from_choice,
                                       'jpg': jpg,
                                       'png': png})

    return gif, gif_from, out1, caption, jpg, png, choose, out2, summary


def set_saving(rootname, xlims, ylims):
    """
    Generates widget to determine directory in
    which to save the frames. If directory does
    not already exists, it will be created. If
    directory does exist, the option to overwrite
    the directory is given.

    Parameters
    ----------
    rootname : str
        Rootname identifier for the current
        observation.
    xlims, ylims : tuples of int


    Returns
    -------
    caption : widgets.widget_string.HTML
    name : widgets.widget_string.Text
    out : widgets.widget_output.Output
    overwrite : widgets.widget_selection.Dropdown
    """
    default_filename = make_default_filename(rootname, xlims, ylims)

    line = 'Set a name for the image frames. This will also be the name of '\
           'the directory in which these frames will be saved. '\
           'You may specify absolute or relative paths if you do not want '\
           'to save in your current working directory.'

    caption = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>'+line+' </p>')

    name = widgets.Text(value=default_filename,
                        description='GIF name: ')
    message = widgets.Label(value='',
                            disabled=True)
    overwrite = widgets.Dropdown(value=False,
                                 options=[True, False],
                                 description='Overwrite: ')

    def check_existing(name):
        """
        Check if path already exists.

        Parameter
        ---------
        name : widgets.widget_string.Text
        """
        if os.path.exists(name):
            message.value = f'Warning: Directory "{name}" already exists.'
            overwrite.disabled = False
            hbox = widgets.HBox([message, overwrite])
            display(hbox)
        else:
            if name == '':
                message.value = 'Please enter a name before proceeding.'
            else:
                if name == default_filename:
                    message.value = f'Default directory "{name}" will be created.'
                else:
                    message.value = f'Directory "{name}" will be created.'
            overwrite.disabled = True
            display(message)

    out = widgets.interactive_output(check_existing, {'name': name})

    return caption, name, out, overwrite

def set_timing():
    """
    Generates widget to adjust timing.

    Returns
    -------
    caption : widgets.widget_string.HTML
    dur :  ``widgets.widget_float.FloatSlider``
        Duration (in seconds) for each frame.
    """
    line = 'Do you want to adjust the duration of each frame? Default is 0.1 seconds (10 frames per second).'
    caption = widgets.HTML(value='<style>p{word-wrap: break-word}</style> <p>'+line+' </p>')

    dur = widgets.FloatSlider(description='Duration (s): ',
                              value=0.10, min=0.01, max=1)

    return caption, dur


# save functions
def make_frames(plot, gif_setup):
    """
    Function to make frames.

    Parameters
    ----------
    plot : tuple
    gif_setup : tuple
    frame_format : str

    Returns
    -------
    file_names : list of str
        List of string representations for the names of
        the plots just created and saved.
    """
    frame_format = gif_setup[3][1].children[1].value.split(' ')[0].lower()

    ax = plot[1]
    w = plot[2]
    filepath = plot[3]
    ext_type = plot[4]

    cmap = w.children[0].value
    lim_slider = w.children[2].value

    rootname, xlims, ylims = get_ax_info(ax)

    save_name = gif_setup[2][1].value
    overwrite = gif_setup[2][3].value

    save_name, overwrite = check_directory(save_name, overwrite)
    fits_file = fits.open(filepath)
    indices = get_indices(fits_file, ext_type)
    rootname = fits_file[0].header['ROOTNAME']

    file_names = []

    for index in indices:
        fig, ax = plt.subplots()
        data, limits = get_data_and_norm_lims(index, fits_file, lim_slider)
        img = ax.imshow(data,
                        origin='lower',
                        cmap=cmap,
                        norm=Normalize(vmin=limits[0], vmax=limits[1]))
        cb = fig.colorbar(mappable=img, label='electrons', ax=ax)
        cb.ax.yaxis.set_major_formatter(tick.FormatStrFormatter('%.2f'))
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        view_title = f'{rootname}: [{ext_type.upper()},{index}]'
        ax.set_title(view_title, fontsize=12)
        plot_name = save_name.split('/')[-1]
        file_name = f'{save_name}/{plot_name}_{index}.{frame_format}'
        plt.savefig(file_name, dpi=150)
        file_names.append(file_name)
        plt.close()

    return file_names


def make_gif(gif_frames, gif_setup):
    """
    Function to make gif from a list of file names.

    Parameters
    ----------
    file_names : list of str
        List of string representations for the names of
        the plots just created and saved.
    gif_setup : tuple
    """
    loop = gif_setup[0][2].value
    duration = gif_setup[1][1].value
    save_name = gif_setup[2][1].value

    gif_name = save_name+'/'+save_name.split('/')[-1]+'.gif'

    with imageio.get_writer(gif_name,
                           mode='I',
                           duration=duration,
                           loop=loop) as writer:
        for gif_frame in gif_frames:
            image = imageio.imread(gif_frame)
            writer.append_data(image)
    print('GIF saved.')

def make_output(plot, gif_setup):
    """
    Function to make the desired output set by `gif_setup`.

    Parameters
    ----------
    plot : tuple
    gif_setup : tuple

    Returns
    -------
    file_names : list of str
        List of string representations for the names of
        the plots just created and saved.
    """
    gif_choice = gif_setup[3][0].children[1].value
    if gif_choice:
        frame_format = gif_setup[3][1].children[1].value
        if frame_format == None:
            frame_format = 'png'
        else:
            frame_format = frame_format[:3].lower()

        gif_frames = make_frames(plot, gif_setup, frame_format)

def check_directory(save_name, overwrite):
    """
    Parameters
    ----------
    save_name : str
    overwrite : Boolean
    """
    if not os.path.exists(save_name):
        os.mkdir(save_name)
        print(f'Made new directory: {save_name}')
    else:
        print(f'Writing to directory: {save_name}')
        if overwrite:
            print(f'Will overwrite any existing files.')
        else:
            print(f'Will not overwrite any existing files.')
    return save_name, overwrite
