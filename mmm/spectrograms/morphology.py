from . import *
from .templates import *


def erosion_geodesic(marker: torch.Tensor, condition: torch.Tensor):
    e = greyscale.erosion(marker, torch.zeros(3, 3, dtype=marker.dtype, device=marker.device))
    return torch.maximum(condition, e)


def dilation_geodesic(marker: torch.Tensor, condition: torch.Tensor):
    d = greyscale.dilation(marker, torch.zeros(3, 3, dtype=marker.dtype, device=marker.device))
    return torch.minimum(condition, d)


def reconstruction_erosion(marker: Optional[torch.Tensor], condition: torch.Tensor, iterations: Optional[int] = None,
                           verbose=False, verbose_it_step=10):
    start = time.time()

    if verbose:
        print('Starting reconstruction by erosion...')

    if marker is None:
        marker = torch.zeros_like(condition)

    x_recons = torch.clone(marker)

    count = 0
    while True:
        x_out = erosion_geodesic(x_recons, condition)

        if torch.all(torch.eq(x_out, x_recons)):
            break
        else:
            x_recons = x_out
        count += 1

        if verbose:
            if count % verbose_it_step == 0:
                print("it:", count)

        if count == iterations:
            break

    if verbose:
        print('Time to apply reconstruction by erosion: %.3f seconds' % (time.time() - start))

    return x_recons


def reconstruction_erosion_stack(marker: Optional[torch.Tensor], condition: torch.Tensor,
                                 max_iterations: int, verbose=False, verbose_it_step=10):
    start = time.time()

    if verbose:
        print('Starting reconstruction by erosion stack...')

    if marker is None:
        marker = torch.zeros_like(condition)

    x_stack = np.zeros((max_iterations, *marker.shape), dtype=np.float32)
    x_stack[0, :, :] = marker.cpu().numpy()

    i = 0
    while True:
        x_in = torch.from_numpy(x_stack[i, :, :]).to(DEVICE)
        x_out = erosion_geodesic(x_in, condition)
        x_stack[i+1, :, :] = x_out.cpu().numpy()

        i += 1

        if i == max_iterations-1 or np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

        if verbose:
            if i % verbose_it_step == 0:
                print("it:", i)

    if verbose:
        print('Time to apply reconstruction by erosion: %.3f seconds' % (time.time() - start))

    return x_stack


def reconstruction_dilation(marker: Optional[torch.Tensor], condition: torch.Tensor, iterations: Optional[int] = None,
                            verbose=False, verbose_it_step=10):
    start = time.time()

    if marker is None:
        marker = torch.zeros_like(condition) - 128
        marker[condition == torch.max(condition)] = torch.max(condition)

    x_recons = torch.clone(marker)

    count = 0
    while True:
        x_out = dilation_geodesic(x_recons, condition)

        if torch.all(torch.eq(x_out, x_recons)):
            break
        else:
            x_recons = x_out
        count += 1

        if verbose:
            if count % verbose_it_step == 0:
                print("it:", count)
                from .plot import plot_two_spectrogram
                from .processing import MIN_DB
                plot_two_spectrogram(marker.cpu().numpy(), x_out.cpu().numpy(),
                                     v_min_1=MIN_DB, v_min_2=MIN_DB, v_max_1=0, v_max_2=0, c_map_1='Greys',
                                     c_map_2='Greys')
                plt.show()

        if count == iterations:
            break

    if verbose:
        print('Time to apply reconstruction by dilation: %.3f seconds' % (time.time() - start))

    return x_recons


def reconstruction_dilation_stack(marker: Optional[torch.Tensor], condition: torch.Tensor, iterations: Optional[int] = None,
                                  verbose=False, verbose_it_step=10):
    start = time.time()

    if verbose:
        print('Starting reconstruction by dilation stack...')

    if marker is None:
        marker = torch.zeros_like(condition) - 128
        marker[condition == torch.max(condition)] = torch.max(condition)

    x_stack = np.zeros((iterations, *marker.shape), dtype=np.float32)
    x_stack[0, :, :] = marker.cpu().numpy()

    i = 0
    while True:
        x_in = torch.from_numpy(x_stack[i, :, :]).to(DEVICE)
        x_out = dilation_geodesic(x_in, condition)
        x_stack[i+1, :, :] = x_out.cpu().numpy()

        i += 1

        if i == iterations-1 or np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

        if verbose:
            if i % verbose_it_step == 0:
                print("it:", i)
                # from .plot import plot_two_spectrogram
                # from .processing import MIN_DB
                # plot_two_spectrogram(marker.cpu().numpy(), x_out.cpu().numpy(),
                #                      v_min_1=MIN_DB, v_min_2=MIN_DB, v_max_1=0, v_max_2=0, c_map_1='Greys',
                #                      c_map_2='Greys')
                # plt.show()

    if verbose:
        print('Time to apply reconstruction by dilation: %.3f seconds' % (time.time() - start))

    return x_stack


def greyscale_hit_or_miss(input_image: torch.Tensor,
                          str_el_in: torch.Tensor,
                          str_el_out: torch.Tensor,
                          origin_in: Optional[Tuple[int, int]] = None,
                          origin_out: Optional[Tuple[int, int]] = None,
                          border: str = 'g',
                          alpha=0) -> torch.Tensor:
    str_el_dil = torch.flip(str_el_out, dims=[0, 1])
    if origin_out is not None:
        origin_out = (str_el_dil.shape[0] - origin_out[0] - 1, str_el_dil.shape[1] - origin_out[1] - 1)
    e = greyscale.erosion(input_image, torch.zeros_like(str_el_in).to(input_image.dtype), str_el_in, origin_in, border)
    d = greyscale.dilation(input_image, torch.zeros_like(str_el_dil).to(input_image.dtype), str_el_dil, origin_out)
    d[torch.isinf(d)] = torch.min(d[torch.logical_not(torch.isinf(d))])

    output = input_image - d
    is_simple = torch.logical_and(torch.greater_equal(e, input_image - alpha), input_image > d)
    output[torch.logical_not(is_simple)] = 0

    return output


def binary_hit_or_miss(input_image: torch.Tensor,
                       str_el_in: torch.Tensor,
                       str_el_out: torch.Tensor,
                       origin_in: Optional[Tuple[int, int]] = None,
                       origin_out: Optional[Tuple[int, int]] = None,
                       border: str = 'g') -> torch.Tensor:
    e = binary.erosion(input_image, str_el_in, origin_in, border)
    d = binary.erosion(~input_image, str_el_out, origin_out, border)
    return torch.logical_and(e, d)


def elementary_greyscale_sequential_thinning(x: torch.Tensor, direction: str = 'a', border='g', alpha=0):
    if direction == 'h':
        x_simple = greyscale_hit_or_miss(x, C_E, D_E, border=border, alpha=alpha)
        x_thin = x - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_W, D_W, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_NW, D_NW, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_SE, D_SE, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_NE, D_NE, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_SW, D_SW, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        return x_thin

    elif direction == 'v':
        x_simple = greyscale_hit_or_miss(x, C_N, D_N, border=border, alpha=alpha)
        x_thin = x - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_S, D_S, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_NE, D_NE, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_SW, D_SW, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_NW, D_NW, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        x_simple = greyscale_hit_or_miss(x_thin, C_SE, D_SE, border=border, alpha=alpha)
        x_thin = x_thin - x_simple

        return x_thin
    else:
        raise ValueError("Parameter 'direction' must be 'h' or 'v'")


def greyscale_thinning(input_image: torch.Tensor, iterations: Optional[int] = None, direction: str = 'a',
                       verbose=False, verbose_it_step=10, alpha=0):
    x_thin = torch.clone(input_image)
    count = 0
    while True:
        x_out = elementary_greyscale_sequential_thinning(x_thin, direction, alpha=alpha)

        if torch.all(torch.eq(x_out, x_thin)):
            break
        else:
            x_thin = x_out
        count += 1

        if verbose:
            if count % verbose_it_step == 0:
                print("it:", count)

        if count == iterations:
            break

    return x_thin


def greyscale_thinning_stack(input_image: torch.Tensor, direction: str = 'a',
                             verbose=False, verbose_it_step=10,
                             max_iterations: Optional[int] = None):
    start = time.time()

    if verbose:
        print('Starting %s thinning stack...' % direction)

    x_stack = np.zeros((max_iterations, *input_image.shape), dtype=np.float32)
    x_stack[0, :, :] = input_image.cpu().numpy()

    i = 0
    while True:
        x_in = torch.from_numpy(x_stack[i, :, :]).to(DEVICE)
        x_out = elementary_greyscale_sequential_thinning(x_in, direction)
        x_stack[i + 1, :, :] = x_out.cpu().numpy()

        if np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

        i += 1

        if verbose:
            if i % verbose_it_step == 0:
                print("it:", i)

        if i == max_iterations-1 or np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

    if verbose:
        print('Time to apply thinning: %.3f seconds' % (time.time() - start))

    return x_stack


def elementary_greyscale_trimming(x: torch.Tensor, direction: str = 'a', border='g', alpha=0):
    if direction == 'h':
        x_simple = greyscale_hit_or_miss(x, C, D_E, border=border, alpha=alpha)
        x_trim = x - x_simple

        x_simple = greyscale_hit_or_miss(x_trim, C, D_W, border=border, alpha=alpha)
        x_trim = x_trim - x_simple

        return x_trim

    elif direction == 'v':
        x_simple = greyscale_hit_or_miss(x, C, D_N, border=border, alpha=alpha)
        x_trim = x - x_simple

        x_simple = greyscale_hit_or_miss(x_trim, C, D_S, border=border, alpha=alpha)
        x_trim = x_trim - x_simple

        return x_trim
    else:
        raise ValueError("Parameter 'direction' must be 'h' or 'v'")


def greyscale_trimming(input_image: torch.Tensor, iterations: Optional[int] = None, direction: str = 'a',
                       verbose=False, verbose_it_step=10, alpha=0):
    x_thin = torch.clone(input_image)
    count = 0
    while True:
        x_out = elementary_greyscale_trimming(x_thin, direction, alpha=alpha)

        if torch.all(torch.eq(x_out, x_thin)):
            break
        else:
            x_thin = x_out
        count += 1

        if verbose:
            if count % verbose_it_step == 0:
                print("it:", count)

        if count == iterations:
            break

    return x_thin


def greyscale_trimming_stack(input_image: torch.Tensor, iterations: Optional[int] = None, direction: str = 'a',
                             verbose=False, verbose_it_step=10, alpha=0):
    start = time.time()

    if verbose:
        print('Starting %s trimming stack...' % direction)

    x_stack = np.zeros((iterations, *input_image.shape), dtype=np.float32)
    x_stack[0, :, :] = input_image.cpu().numpy()

    i = 0
    while True:
        x_in = torch.from_numpy(x_stack[i, :, :]).to(DEVICE)
        x_out = elementary_greyscale_trimming(x_in, direction, alpha=alpha)
        x_stack[i+1, :, :] = x_out.cpu().numpy()

        if np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

        i += 1

        if verbose:
            if i % verbose_it_step == 0:
                print("it:", i)

        if i == iterations-1 or np.all(np.equal(x_stack[i+1, :, :], x_stack[i, :, :])):
            break

    if verbose:
        print('Time to apply trimming: %.3f seconds' % (time.time() - start))

    return x_stack


def binary_thinning(image_input: torch.Tensor, iterations: Optional[int] = None, direction: str = 'h',
                    verbose=False, verbose_it_step=10):
    x_thin = torch.clone(image_input)
    count = 0
    while True:
        x_out = elementary_binary_thinning(x_thin, direction)
        if torch.all(torch.eq(x_out, x_thin)):
            break
        else:
            x_thin = x_out
        count += 1

        if verbose:
            if count % verbose_it_step == 0:
                print("it:", count)

        if count == iterations:
            break

    return x_thin


def elementary_binary_thinning(x: torch.Tensor, direction: str = 'h', border='g'):
    if direction == 'h':
        x_simple = binary_hit_or_miss(x, C_E, D_E, border=border)
        x_thin = torch.logical_and(x, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_W, D_W, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_NW, D_NW, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_SE, D_SE, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_NE, D_NE, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_SW, D_SW, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        return x_thin
    elif direction == 'v':
        x_simple = binary_hit_or_miss(x, C_N, D_N, border=border)
        x_thin = torch.logical_and(x, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_S, D_S, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_NE, D_NE, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_SW, D_SW, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_NW, D_NW, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        x_simple = binary_hit_or_miss(x_thin, C_SE, D_SE, border=border)
        x_thin = torch.logical_and(x_thin, torch.logical_not(x_simple))

        return x_thin
    else:
        raise ValueError("Parameter 'direction' must be 'h' or 'v'")


def skeleton(image_input, shape=(3, 3), n_max=None):
    str_el = torch.ones(shape, dtype=torch.bool).to(image_input.device)

    result = torch.zeros_like(image_input)
    tmp = torch.clone(image_input)

    n = 1
    while torch.any(tmp):
        opening = binary.opening(tmp, str_el)
        top_hat = torch.logical_and(tmp, torch.logical_not(opening))
        result = torch.logical_or(result, top_hat)

        tmp = binary.erosion(tmp, str_el)

        n += 1
        if n_max is not None:
            if n > n_max:
                break

    return result


def remove_isolated_greyscale(input_image: torch.Tensor):
    d = greyscale.dilation(input_image, torch.zeros_like(B_O, dtype=input_image.dtype), B_O)
    e = greyscale.erosion(input_image, torch.zeros_like(B_O, dtype=input_image.dtype), B_O, border='g')
    is_plateau = torch.eq(d, e)
    is_bigger = torch.gt(input_image, d)

    is_isolated = torch.logical_and(is_plateau, is_bigger)

    input_image[is_isolated] = d[is_isolated]
