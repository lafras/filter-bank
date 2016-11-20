from numpy import pi

import click

import filters
import noisy_signal


@click.group(
    chain=True,
    invoke_without_command=True
)
@click.option(
    '-e',
    '--end',
    type=float,
    default=3*pi
)
@click.option(
    '-i',
    '--input',
    type=click.File('r')
)
@click.option(
    '-s',
    '--steps',
    type=int,
    default=10**4
)
def cli(end, input, steps):
    pass


@cli.resultcallback()
def process_pipeline(processors, end, input, steps):

    for processor in processors:
        input = processor(input)

    click.echo(
        input.head()
    )

@cli.command()
@click.pass_context
def noise(ctx):
    
    end = ctx.parent.params['end']
    steps = ctx.parent.params['steps']

    def processor(frame):
        frame = noisy_signal.noisy_signal(end, steps)
        return frame
    return processor


@cli.command()
@click.option(
    '-r',
    '--remove',
    type=float,
    default=1/7
)
@click.option(
    '-b',
    '--band',
    type=(float, float),
    default=(1/14, 6/7)
)
@click.pass_context
def filter(ctx, band, remove):
    
    end = ctx.parent.params['end']
    steps = ctx.parent.params['steps']
    
    sampling = (steps-1)/end

    def processor(frame):
        bandstop = filters.BandStop(
            remove, sampling, band
        )
        frame['seasonless'] = bandstop(
            frame['signal'].values
        )
        return frame
    return processor


if __name__ == '__main__':
    cli()

