import sky


def make_application():
    """A simple application: jupyter notebook on current workspace."""

    with sky.Dag() as dag:

        setup = 'pip install --upgrade pip && \
        conda init bash && \
        conda activate jupyter || \
          (conda create -n jupyter python=3.9 -y && \
           conda activate jupyter && \
           pip install jupyter)'

        run = f'jupyter notebook --port 8888'

        # Use 'ray attach --port-forward=8888 <config_file>' to forward port to local.
        # e.g., for AWS, 'ray attach --port-forward=8888 config/aws-ray.yml'
        jupyter = sky.Task('jupyter',
                           run=run,
                           setup=setup,
                           workdir='~/local/workspace')

        jupyter.set_resources({
            sky.Resources(accelerators='K80', use_spot=True),
        })

    return dag


dag = make_application()
sky.execute(dag)