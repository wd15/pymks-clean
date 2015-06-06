import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import itertools
import warnings

warnings.filterwarnings("ignore")


def _set_colors():
    """
    Helper function used to set the color map.
    """
    HighRGB = np.array([26, 152, 80]) / 255.
    MediumRGB = np.array([255, 255, 191]) / 255.
    LowRGB = np.array([0, 0, 0]) / 255.
    cdict = _set_cdict(HighRGB, MediumRGB, LowRGB)
    plt.register_cmap(name='PyMKS', data=cdict)
    plt.set_cmap('PyMKS')


def _get_response_cmap():
    """
    Helper function used to set the response color map.

    Returns:
        dictionary with colors and localizations on color bar.
    """
    HighRGB = np.array([26, 152, 80]) / 255.
    MediumRGB = np.array([255, 255, 191]) / 255.
    LowRGB = np.array([0, 0, 0]) / 255.
    cdict = _set_cdict(HighRGB, MediumRGB, LowRGB)
    return colors.LinearSegmentedColormap('coeff_cmap', cdict, 256)


def _get_diff_cmap():
    """
    Helper function used to set the difference color map.

    Returns:
        dictionary with colors and localizations on color bar.
    """
    HighRGB = np.array([118, 42, 131]) / 255.
    MediumRGB = np.array([255, 255, 191]) / 255.
    LowRGB = np.array([0, 0, 0]) / 255.
    cdict = _set_cdict(HighRGB, MediumRGB, LowRGB)
    return colors.LinearSegmentedColormap('diff_cmap', cdict, 256)


def _grid_matrix_cmap():
    """
    Helper function used to set the grid matrix color map.

    Returns:
        dictionary with colors and localizations on color bar.
    """
    HighRGB = np.array([255, 255, 255]) / 255.
    MediumRGB = np.array([150, 150, 150]) / 255.
    LowRGB = np.array([0, 0, 0]) / 255.
    cdict = _set_cdict(HighRGB, MediumRGB, LowRGB)
    return colors.LinearSegmentedColormap('diff_cmap', cdict, 256)


def _set_cdict(HighRGB, MediumRGB, LowRGB):
    """
    Helper function used to set color map from 3 RGB values.

    Args:
        HighRGB: RGB with highest values
        MediumRGB: RGB with medium values
        LowRGB: RGB with lowest values

    Returns:
        dictionary with colors and localizations on color bar.
    """
    cdict = {'red': ((0.0, LowRGB[0], LowRGB[0]),
                     (0.5, MediumRGB[0], MediumRGB[0]),
                     (1.0, HighRGB[0], HighRGB[0])),

             'green': ((0.0, LowRGB[1], LowRGB[1]),
                       (0.5, MediumRGB[1], MediumRGB[1]),
                       (1.0, HighRGB[1], HighRGB[1])),

             'blue': ((0.0, LowRGB[2], LowRGB[2]),
                      (0.5, MediumRGB[2], MediumRGB[2]),
                      (1.0, HighRGB[2], HighRGB[2]))}

    return cdict


def _get_coeff_cmap():
    """
    Helper function used to set the influence coefficients color map.

    Returns
    """
    HighRGB = np.array([244, 109, 67]) / 255.
    MediumRGB = np.array([255, 255, 191]) / 255.
    LowRGB = np.array([0, 0, 0]) / 255.
    cdict = _set_cdict(HighRGB, MediumRGB, LowRGB)
    return colors.LinearSegmentedColormap('coeff_cmap', cdict, 256)


def _get_color_list(n_sets):
    """
    color list for dimensionality reduction plots

    Args:
        n_sets: number of dataset

    Returns:
        list of colors for n_sets
    """
    color_list = ['#1a9850', '#f46d43', '#762a83', '#1a1a1a',
                  '#ffffbf', '#a6d96a', '#c2a5cf', '#878787']
    return color_list[:n_sets]


def draw_microstructure_discretization(M, a=0, s=0, Nbin=6,
                                       bound=0.016, height=1.7, ax=None):
    """ Creates a diagram to illustrate the binning of a continues values
    in local state space.

    Args:
        Array representing a microstructure with a continuous variable.

    Returns:
        Image of the continuous local state binned discretely in the local
        state space.
    """
    if ax is not None:
        ax = plt.axes()
    dx = 1. / (Nbin - 1.)

    cm = plt.get_cmap('cubehelix')
    cNorm = colors.Normalize(vmin=0, vmax=Nbin - 1)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    for i in range(Nbin - 1):
        color = scalarMap.to_rgba(i)
        r = plt.Rectangle((i * dx, 0), dx, dx, lw=4, ec='k', color=color)
        ax.add_patch(r)

    plt.yticks(())

    plt.ylim(ymax=dx * height, ymin=-bound)
    plt.xlim(xmin=-bound, xmax=1 + bound)

    ax.set_aspect('equal')
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    for line in ax.xaxis.get_ticklines():
        line.set_markersize(0)

    all_spines = ['top', 'bottom', 'right', 'left']
    for spline in all_spines:
        ax.spines[spline].set_visible(False)

    plt.xlabel(r'$\chi^h \;\; \left( H = 6 \right)$', fontsize=16)

    v = M[a, s]

    H = np.linspace(0, 1, Nbin)
    m = np.maximum(1 - abs(v - H) / dx, 0)
    Mstring = r'$m_{{{a},{s}}}={v:1.2g}$'.format(a=a, s=s, v=v)
    arr = r'{0:1.2g}'.format(m[0])
    for i in range(1, len(m)):
        arr += r', {0:1.2g}'.format(m[i])
    mstring = r'$m_{{{a},{s}}}^h=\left({arr}\right)$'.format(a=a, s=s, arr=arr)

    plt.plot((v, v), (0, dx * height), 'r--', lw=3)
    plt.text(v + 0.02,
             dx * (1 + 0.65 * (height - 1)),
             Mstring,
             fontsize=16,
             color='r')
    plt.text(v + 0.02,
             dx * (1 + 0.2 * (height - 1)),
             mstring,
             fontsize=16,
             color='r')


def draw_coeff(coeff, fontsize=15):
    """
    Visualize influence coefficients.

    Args:
        coeff: influence coefficients with dimensions (x, y, n_states)
        fontsize - scalar values used for the title font size
    """
    coeff_cmap = _get_coeff_cmap()
    n_coeff = coeff.shape[-1]
    titles = [r'Influence Coefficients $l = %s$' % ii for ii
              in np.arange(n_coeff)]
    _draw_fields(np.rollaxis(coeff, -1, 0), coeff_cmap,
                 fontsize=fontsize, titles=titles)


def draw_microstructure_strain(microstructure, strain):
    """
    Draw microstructure and its associated strain

    Args:
        microstructure - numpy array with dimensions (x, y)
        strain - numpy array with dimensions (x, y)
    """
    plt.close('all')
    cmap = _get_response_cmap()
    fig = plt.figure(figsize=(8, 4))
    ax0 = plt.subplot(1, 2, 1)
    ax0.imshow(microstructure.swapaxes(0, 1), cmap=plt.cm.gray,
               interpolation='none')
    ax0.set_xticks(())
    ax0.set_yticks(())
    ax1 = plt.subplot(1, 2, 2)
    im1 = ax1.imshow(strain.swapaxes(0, 1), cmap=cmap, interpolation='none')
    ax1.set_xticks(())
    ax1.set_yticks(())
    ax1.set_title(r'$\mathbf{\varepsilon_{xx}}$', fontsize=25)
    ax0.set_title('Microstructure', fontsize=20)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([1.0, 0.05, 0.05, 0.9])
    fig.colorbar(im1, cax=cbar_ax)
    plt.tight_layout()
    plt.show()


def draw_microstructures(*microstructures):
    """
    Draw microstructures

    Args:
        microstructures - numpy array with dimensions (n_samples, x, y)
    """
    cmap = plt.cm.gray
    titles = [' ' for s in np.arange(microstructures[0].shape[0])]
    _draw_fields(microstructures[0], cmap, 10, titles)


def draw_strains(strains, titles=None, fontsize=15):
    """
    Draw strain fields

    Args:
        strains - numpy arrays with dimensions (n_samples, x, y)
        titles - list of titles for strain fields
        fontsize - scalar values used for the title font size
    """
    cmap = _get_response_cmap()
    if titles is None:
        titles = [' ' for s in strains]
    _draw_fields(strains, cmap, fontsize, titles)


def draw_concentrations(concentrations, titles=None, fontsize=15):
    """
    Draw comparison fields

    Args:
        concentrations - list of numpy arrays with dimensions (x, y)
        titles - list of titles for concentrations
        fontsize - scalar values used for the title font size
    """
    if titles is None:
        titles = [" " for s in concentrations]
    cmap = _get_response_cmap()
    _draw_fields(concentrations, cmap, fontsize, titles)


def draw_strains_compare(strain_FEM, strain_MKS, fontsize=20):
    """
    Draw comparison of strain fields.

    Args:
        strain_FEM - numpy arrays with dimensions (x, y) from finite element
        strain_MKS - numpy arrays with dimensions (x, y) from MKS
        fontsize - scalar values used for the title font size
    """
    cmap = _get_response_cmap()
    titles = ['Finite Element', 'MKS']
    titles_ = [r'$\mathbf{\varepsilon_{xx}}$ - %s' % title for title in titles]
    _draw_fields((strain_FEM, strain_MKS), cmap, fontsize, titles_)


def draw_concentrations_compare(con1, con2, fontsize=15):
    """
    Draw comparesion of concentrations.

    Args:
        differences - list of difference arrays with dimensions (x, y)
        titles - list of titles for difference arrays
        fontsize - scalar values used for the title font size
    """
    titles = ['Simulation', 'MKS']
    cmap = _get_response_cmap()
    _draw_fields((con1, con2), cmap, fontsize, titles)


def draw_differences(differences, titles=None, fontsize=15):
    """
    Draw differences in predicted response fields.

    Args:
        differences - list of difference arrays with dimesions (x, y)
        titles - list of titles for difference arrays
        fontsize - scalar values used for the title font size
    """
    cmap = _get_diff_cmap()
    if titles is None:
        titles = [' ' for s in differences]
    _draw_fields(differences, cmap, fontsize, titles)


def _draw_fields(fields, field_cmap, fontsize, titles):
    """
    Helper function used to draw fields.

    Args:
        fields - iterable object with 2D numpy arrays
        field_cmap - color map for plot
        fontsize - font size for titles and color bar text
        titles - titles for plot
    """
    vmin = np.min(fields)
    vmax = np.max(fields)
    n_fields = len(fields)
    if titles is not None:
        n_titles = len(titles)
        if n_fields != n_titles:
            raise RuntimeError(
                "number of plots does not make number of titles.")
    plt.close('all')
    fig, axs = plt.subplots(1, n_fields, figsize=(n_fields * 4, 4))
    if n_fields > 1:
        for field, ax, title in zip(fields, axs.flat, titles):
            im = ax.imshow(field.swapaxes(0, 1),
                           cmap=field_cmap, interpolation='none',
                           vmin=vmin, vmax=vmax)
            ax.set_xticks(())
            ax.set_yticks(())
            ax.set_title(title, fontsize=fontsize)
    else:
        im = axs.imshow(fields[0].swapaxes(0, 1), cmap=field_cmap,
                        interpolation='none', vmin=vmin, vmax=vmax)
        axs.set_xticks(())
        axs.set_yticks(())
        axs.set_title(titles[0], fontsize=fontsize)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([1.0, 0.05, 0.05, 0.9])
    cbar_font = np.floor(0.8 * fontsize)
    cbar_ax.tick_params(labelsize=cbar_font)
    cbar_ax.yaxis.set_offset_position('right')
    fig.colorbar(im, cax=cbar_ax)
    plt.tight_layout()
    plt.rc('font', **{'size': str(cbar_font)})
    plt.show()


def draw_gridscores(grid_scores, param, score_label='', colors=('#1a9641',),
                    data_labels=[None], param_label='', fontsize=20):
    """
    Visualize the score values and standard deviations from grids
    scores result from GridSearchCV while varying 1 parameters.

    Args:
        grid_scores: list of grid_scores_ attribute from GridSearchCV
        param: list of parameters used in grid_scores
        score_label: label for score value axis
        colors: list of colors used for this specified parameter
        param_label: list of parameter titles to appear on plot
    """
    if type(grid_scores[0]) is not list:
        grid_scores = [grid_scores]
    if len(grid_scores) != len(data_labels) or len(data_labels) != len(colors):
        raise RuntimeError(
            "grid_scores, colors, and param_lables must have the same length.")
    for grid_score, data_label, color in zip(grid_scores, data_labels, colors):
        tmp = [[params[param], mean_score, scores.std()]
               for params, mean_score, scores in grid_score]
        param_, errors, stddev = list(zip(*tmp))
        plt.fill_between(param_, np.array(errors) - np.array(stddev),
                         np.array(errors) + np.array(stddev), alpha=0.1,
                         color=color)
        plt.plot(param_, errors, 'o-', color=color, label=data_label,
                 linewidth=2)
    if data_labels[0] is not None:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel(score_label, fontsize=fontsize)
    plt.xlabel(param_label, fontsize=fontsize)
    plt.show()


def draw_gridscores_matrix(grid_scores, params, score_label='R-Squared',
                           param_labels=['', '']):
    """
    Visualize the score value matrix and standard deviation matrix from grids
    scores result from GridSearchCV while varying 2 parameters.

    Args:
        grid_scores: grid_scores_ attribute from GridSearchCV
        params: list of 2 parameters used in grid_scores
        score_label: label for score value axis
        param_labels: list of parameter titles to appear on plot
    """
    tmp = [[params, mean_score, scores.std()]
           for parameters, mean_score, scores in grid_scores.grid_scores_]
    param, means, stddev = list(zip(*tmp))
    param_range_0 = grid_scores.param_grid[params[0]]
    param_range_1 = grid_scores.param_grid[params[1]]
    mat_size = (len(param_range_1), len(param_range_0))
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    matrices = np.concatenate((np.array(means).reshape(mat_size)[None],
                               np.array(stddev).reshape(mat_size)[None]))
    X_cmap = _grid_matrix_cmap()
    x_label = param_labels[0]
    y_label = param_labels[1]
    plot_title = [score_label, 'Standard Deviation']
    for ax, label, matrix, title in zip(axs, param_labels,
                                        np.swapaxes(matrices, -1, -2),
                                        plot_title):
        ax.set_xticklabels(param_range_0, fontsize=12)
        ax.set_yticklabels(param_range_1, fontsize=12)
        ax.set_xticks(np.arange(len(param_range_0)))
        ax.set_yticks(np.arange(len(param_range_0)))
        ax.set_xlabel(x_label, fontsize=14)
        ax.set_ylabel(y_label, fontsize=14)
        im = ax.imshow(np.swapaxes(matrix, 0, 1),
                       cmap=X_cmap, interpolation='none')
        ax.set_title(title, fontsize=22)
        divider = make_axes_locatable(ax)
        cbar_ax = divider.append_axes("right", size="10%", pad=0.05)
        cbar = plt.colorbar(im, cax=cbar_ax)
        cbar.ax.tick_params(labelsize=12)
        fig.subplots_adjust(right=1.2)
    plt.show()


def draw_component_variance(variance):
    """
    Visualize the percent variance as a function of components.

    Args:
        variance: variance ration explanation function for dimensional
            reduction technique.
    """
    plt.plot(np.cumsum(variance * 100), 'o-', color='#1a9641', linewidth=2)
    plt.xlabel('Number of Components', fontsize=15)
    plt.ylabel('Percent Variance', fontsize=15)
    plt.show()


def bin(arr, n_bins):
    """
    Discretize the array `arr`, which must be between 0 and 1.

    >>> res = bin(np.array((0.2, 0.5, 0.7)), 4)
    >>> np.allclose(res,
    ...             [[ 0.4,  0.6,  0. ,  0. ],
    ...              [ 0. ,  0.5,  0.5,  0. ],
    ...              [ 0. ,  0. ,  0.9,  0.1]])
    True

    Args:
        arr: Array that must be between 0 and 1.
        n_bins: Integer value representing the number of local states
             in the local state space of the microstructure function.

    Returns:
        Microstructure function for array `arr`.
    """
    X = np.linspace(0, 1, n_bins)
    dX = X[1] - X[0]

    return np.maximum(1 - abs(arr[:, None] - X) / dX, 0)


def draw_components(*X, **labels):
    """
    Visualize low dimensional representations of microstructures.

    Args:
        X: arrays with low dimensional data with dimensions [n_samplles,
            n_componts]. The length of n_components must be 2 or 3.
        labels: labes for each of each array X

    """
    size = np.array(X[0].shape)
    if size[-1] == 2:
        _draw_components_2D(X, labels)
    elif size[-1] == 3:
        _draw_components_3D(X, labels)
    else:
        raise RuntimeError("n_components must be 2 or 3.")


def _draw_components_2D(X, labels):
    """
    Helper function to plot 2 components.

    Args:
        X: Arrays with low dimensional data
        labels: labels for each of the low dimensional arrays
    """
    n_sets = len(X)
    color_list = _get_color_list(n_sets)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Component 1', fontsize=15)
    ax.set_ylabel('Component 2', fontsize=15)
    ax.set_xticks(())
    ax.set_yticks(())
    X_array = np.concatenate(X)
    x_min, x_max = [np.min(X_array[:, 0]), np.max(X_array[:, 0])]
    y_min, y_max = [np.min(X_array[:, 1]), np.max(X_array[:, 1])]
    x_epsilon = (x_max - x_min) * 0.05
    y_epsilon = (y_max - y_min) * 0.05
    ax.set_xlim([x_min - x_epsilon, x_max + x_epsilon])
    ax.set_ylim([y_min - y_epsilon, y_max + y_epsilon])
    for key, n in zip(labels.keys(), np.arange(n_sets)):
        ax.plot(X[n][:, 0], X[n][:, 1], 'o', color=color_list[n],
                label=labels[key])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Low Dimensional Representation', fontsize=20)
    plt.show()


def _draw_components_3D(X, labels):
    """
    Helper function to plot 2 components.

    Args:
        X: Arrays with low dimensional data
        labels: labels for each of the low dimensional arrays
    """
    n_sets = len(X)
    color_list = _get_color_list(n_sets)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Component 1', fontsize=10)
    ax.set_ylabel('Component 2', fontsize=10)
    ax.set_zlabel('Component 3', fontsize=10)
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_zticks(())
    X_array = np.concatenate(X)
    x_min, x_max = [np.min(X_array[:, 0]), np.max(X_array[:, 0])]
    y_min, y_max = [np.min(X_array[:, 1]), np.max(X_array[:, 1])]
    z_min, z_max = [np.min(X_array[:, 2]), np.max(X_array[:, 2])]
    x_epsilon = (x_max - x_min) * 0.05
    y_epsilon = (y_max - y_min) * 0.05
    z_epsilon = (z_max - z_min) * 0.05
    ax.set_xlim([x_min - x_epsilon, x_max + x_epsilon])
    ax.set_ylim([y_min - y_epsilon, y_max + y_epsilon])
    ax.set_zlim([z_min - z_epsilon, z_max + z_epsilon])
    for key, n in zip(labels.keys(), np.arange(n_sets)):
        ax.plot(X[n][:, 0], X[n][:, 1], X[n][:, 2], 'o', color=color_list[n],
                label=labels[key])
    plt.title('Low Dimensional Representation', fontsize=15)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


def draw_goodness_of_fit(fit_data, pred_data, labels):
    """
    Visualize goodness of fit plot for MKSHomogenizationModel.

    Args:
        fit_data: Low dimensional data used to fit the MKSHomogenizationModel
        pred_data: Low dimensional data used for prediction
    """
    y_total = np.concatenate((fit_data, pred_data), axis=-1)
    y_min, y_max = np.min(y_total), np.max(y_total)
    middle = (y_max + y_min) / 2.
    data_range = y_max - y_min
    line = np.linspace(middle - data_range * 1.03 / 2,
                       middle + data_range * 1.03 / 2, endpoint=False)
    plt.plot(line, line, '-', linewidth=3, color='#000000')
    plt.plot(fit_data[0], fit_data[1], 'o', color='#1a9850', label=labels[0])
    plt.plot(pred_data[0], pred_data[1], 'o',
             color='#f46d43', label=labels[1])
    plt.title('Goodness of Fit', fontsize=20)
    plt.xlabel('Actual', fontsize=15)
    plt.ylabel('Predicted', fontsize=15)
    plt.legend(loc=2)
    plt.show()


def _get_correlation_titles(correlation_labels, selected_labels):
    """
    Helper function to get the correct spatial correlation keys.

    >>> corr_dict = {'(1, 1)': np.ones((3, 3)), '(2, 1)':np.zeros((3, 3))}
    >>> corr_plots = [(1, 1), (1, 2)]
    >>> result = ['(1, 1)', '(2, 1)']
    >>> assert result == _get_correlation_titles(corr_dict, corr_plots)

    Args:
        correlation_dict: dictionary that has spatial correlation lab as
            keys and spatial correlations as values
        selected_correlation_plots: list of correlations that will be drawn.

    Returns:
        list of correlation computed with local state labels in the correct
            order.
    """
    if selected_labels is None:
        return None
    selected_labels = map(str, selected_labels)
    new_names = selected_labels
    for plot_name in selected_labels:
        if plot_name not in correlation_labels:
            name = list(plot_name)
            name[1], name[4] = name[4], name[1]
            new_name = ''.join(str(e) for e in name)
            new_names[new_names.index(plot_name)] = new_name
            if new_name not in correlation_labels:
                raise RuntimeError(str(plot_name) + " correlation not found", )
    return new_names


def _get_autocorrelation_titles(n_states):
    """
    Helper function to get the autocorrelations computed and returns them in
    a list.

    >>> result = [(1, 1), (2, 2), (3, 3), (4, 4)]
    >>> assert result == _get_autocorrelation_titles(4)

    Args:
        n_states: number of local states

    Returns:
        list of computed autocorrelations
    """
    states = np.arange(n_states) + 1
    return list(zip(states, states))


def _get_crosscorrelation_titles(n_states):
    """
    Helper function to get the crosscorrelations computed and returns them in
    a list.

    >>> result = [(1, 4), (2, 1), (3, 2), (4, 3), (1, 3), (2, 4)]
    >>> assert result == _get_crosscorrelation_titles(4)

    Args:
        n_states: number of local states

    Returns:
        list of computed crosscorrelations
    """

    states = np.arange(n_states) + 1
    Niter = n_states / 2
    Nslice = n_states * (n_states - 1) / 2
    tmp = [zip(states, np.roll(states, i)) for i in range(1, Niter + 1)]
    titles = list(itertools.chain.from_iterable(tmp))
    return titles[:Nslice]


def draw_correlations(X_corr, correlations=None):
    """
    Visualize spatial correlations.

    Args:
        X_corr: correlations
        correlations: correlations that will be displayed.
    """
    n_states = ((np.sqrt(8 * X_corr.shape[-1] + 1) - 1) / 2).astype(int)
    X_auto_lists = _get_autocorrelation_list(X_corr[..., :n_states])
    X_cross_lists = _get_crosscorrelation_list(X_corr[..., n_states:])
    X_corr_lists = [X_auto_lists[0] + X_cross_lists[0],
                    np.concatenate((X_auto_lists[1],X_cross_lists[1]),
                    axis=-1)]
    _draw_stats(X_corr_lists, correlations=correlations)


def draw_autocorrelations(X_auto, correlations=None):
    """
    Visualize spatial autocorrelations.

    Args:
        X_auto: autocorrelations
        correlations: correlations that will be displayed.
    """
    X_auto_lists = _get_autocorrelation_list(X_auto)
    _draw_stats(X_auto_lists, correlations=correlations)


def draw_crosscorrelations(X_cross, correlations=None):
    """
    Visualize spatial crosscorrelations.

    Args:
        X_cross: crosscorrelations
        correlations: correlations that will be displayed.
    """
    X_cross_lists = _get_crosscorrelation_list(X_cross)
    _draw_stats(X_cross_lists, correlations=correlations)


def _get_autocorrelation_list(X_auto):
    """
    Helper function to label autocorrelations.

    >>> X_auto = np.ones((3, 3, 2))
    >>> X_auto[..., 1] = 2.
    >>> X_auto_list = _get_autocorrelation_list(X_auto)
    >>> X_result = [['(1, 1)', '(2, 2)'],
    ...             np.concatenate([X_auto[..., 0][..., None],
    ...                             X_auto[..., 1][..., None]], axis=-1)]
    >>> assert X_result[0] == X_auto_list[0]
    >>> assert np.allclose(X_result[1], X_auto_list[1])

    Args:
        X_auto: autocorrelations

    Returns:
        nested list with the local states labels and the spatial
        correlations
    """
    auto_labels = map(str, _get_autocorrelation_titles(X_auto.shape[-1]))
    return [auto_labels, X_auto]


def _get_crosscorrelation_list(X_cross):
    """
    Helper function to label autocorrelations.

    >>> X_cross = np.zeros((3, 3, 3))
    >>> X_cross[..., 1] = 1
    >>> X_cross[..., 2] = 2
    >>> X_cross_list = _get_crosscorrelation_list(X_cross)
    >>> X_result = [['(1, 3)', '(2, 1)', '(3, 2)'],
    ...             np.concatenate([X_cross[..., 0][..., None],
    ...                             X_cross[..., 1][..., None],
    ...                             X_cross[..., 2][..., None]], axis=-1)]
    >>> assert X_result[0] == X_cross_list[0]
    >>> assert np.allclose(np.concatenate(X_result[1]),
    ...                    np.concatenate(X_cross_list[1]))

    Args:
        X_cross: crosscorrelations

    Returns:
        nested list with the local states labels and the spatial
        correlations
    """
    n_states = 0.5 + np.sqrt(1 + 8 * X_cross.shape[-1]) / 2.
    cross_labels = map(str, _get_crosscorrelation_titles(int(n_states)))
    return [cross_labels, X_cross]


def _draw_stats(X_lists, correlations=None):
    """
    Helper function used by visualize the spatial correlations.

    Args:
        X_lists: nested list with the local states labels and the spatial
             correlations
        correlations: list of tuples to select the spatial correlations
            that will be displayed.
    """
    X_cmap = _get_coeff_cmap()
    plt.close('all')
    correlation_labels = _get_correlation_titles(X_lists[0], correlations)
    if correlation_labels is None:
        correlation_labels = X_lists[0]
    n_plots = len(correlation_labels)
    X_corr_index = [X_lists[0].index(s) for s in correlation_labels]
    X_list = [X_lists[1][..., s] for s in X_corr_index]
    X_ = np.concatenate(tuple(X_list))
    vmin = np.min(X_)
    vmax = np.max(X_)
    x_loc, x_labels = _get_ticks_params(X_.shape[0])
    y_loc, y_labels = _get_ticks_params(X_.shape[1])
    fig, axs = plt.subplots(1, n_plots, figsize=(n_plots * 5, 5))
    if n_plots == 1:
        axs = list([axs])
    for ax, label, img in zip(axs, correlation_labels, X_list):
        ax.set_xticks(x_loc)
        ax.set_xticklabels(x_labels, fontsize=12)
        ax.set_yticks(y_loc)
        ax.set_yticklabels(y_labels, fontsize=12)
        im = ax.imshow(np.swapaxes(img, 0, 1), cmap=X_cmap,
                       interpolation='none', vmin=vmin, vmax=vmax)
        ax.set_title(r"Correlation $l = {0}$, $l' = {1}$".format(label[1],
                                                                 label[-2]),
                     fontsize=15)
        fig.subplots_adjust(right=0.8)
        divider = make_axes_locatable(ax)
        cbar_ax = divider.append_axes("right", size="10%", pad=0.05)
        cbar_ticks = _get_colorbar_ticks(img, 5)
        cbar_ticks_diff = cbar_ticks[-1] - cbar_ticks[0]
        cbar = plt.colorbar(im, cax=cbar_ax, ticks=cbar_ticks,
                            boundaries=np.arange(cbar_ticks[0],
                                                 cbar_ticks[-1] + 0.005,
                                                 cbar_ticks_diff * 0.005))
        cbar.ax.tick_params(labelsize=12)
        fig.subplots_adjust(right=0.8)
        plt.tight_layout()
    plt.show()


def _get_ticks_params(l):
    """
    Helper function used to tick locations and lables for spatila correlation
    plots.

    >>> l = 4
    >>> result = ([0, 1, 2, 3, 4], [-2, -1, 0, 1, 2])
    >>> assert result == _get_ticks_params(l)

    Args:
        l: shape of array along the axis
    """
    segments = np.roll(np.arange(4, 7, dtype=int), 1, 0)
    m = segments[np.argmin(l % segments)]
    n = max((l + 1) / m, 1)
    tick_loc = range(0, l + n, n)
    tick_labels = range(- (l - 1) / 2, (l + 1) / 2 + n, n)
    return tick_loc, tick_labels


def _get_colorbar_ticks(X_, n_ticks):
    """
    Helper function to get colorbar color tick locations.

    Args:
        X: sspatial correlations array
           (n_samples, x,  y, local_state_correlation)
    """
    tick_range = np.linspace(np.min(X_), np.max(X_), n_ticks)
    return tick_range.astype(float)


def draw_learning_curves(estimator, X, y, ylim=None, cv=None, n_jobs=1,
                         scoring=None, train_sizes=np.linspace(.1, 1.0, 5)):
    """Code taken from scikit-learn examples for version 0.15.

    Generate a simple plot of the test and traning learning curve.

    Args:
        estimator : object type that implements the "fit" and "predict" methods
            An object of that type which is cloned for each validation.
        title: string
            Used for the title for the chart.
        X: array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.
        y: array-like, shape (n_samples) or (n_samples, n_features), optional
            Target relative to X for classification or regression;
            None for unsupervised learning.
        ylim : tuple, shape (ymin, ymax), optional
            Defines minimum and maximum yvalues plotted.
        cv : integer, cross-validation generator, optional
            If an integer is passed, it is the number of folds (defaults to 3).
            Specific cross-validation objects can be passed, see
            sklearn.cross_validation module for the list of possible objects
        n_jobs : integer, optional
            Number of jobs to run in parallel (default 1).
        train_sizes : array-like, shape (n_ticks,), dtype float or int
            Relative or absolute numbers of training examples that will be used
            to generate the learning curve. If the dtype is float, it is
            regarded as a fraction of the maximum size of the training set
            (that is determined by the selected validation method), i.e. it has
            to be within (0, 1]. Otherwise it is interpreted as absolute sizes
            of the training sets. Note that for classification the number of
            samples usually have to be big enough to contain at least one
            sample from each class. (default: np.linspace(0.1, 1.0, 5))

        Returns:
            A plot of the learning curves for both the training curve and the
            cross-validation curve.
    """
    from sklearn.learning_curve import learning_curve

    flat_shape = (X.shape[0],) + (np.prod(X.shape[1:]),)
    X_flat = X.reshape(flat_shape)
    plt.figure()
    plt.title('Learning Curves', fontsize=20)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples", fontsize=15)
    plt.ylabel("Score", fontsize=15)
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X_flat, y, cv=cv, n_jobs=n_jobs,
        train_sizes=train_sizes, scoring=scoring)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="#f46d43")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1,
                     color="#1a9641")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="#f46d43",
             linewidth=2, label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="#1a9641",
             linewidth=2, label="Cross-validation score")

    plt.legend(loc="best")
    plt.show()
