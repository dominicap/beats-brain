from azureml.core import Workspace
ws = Workspace.create(name='beatsBrain-local4',
                      subscription_id='66f8937f-1057-4155-aefd-52c32c7de0d5',
                      resource_group='beats-brain',
                      create_resource_group=False,
                      location='eastus2',
                      exist_ok = True
                     )

#ws.write_config(path="./Beats-Brain/lib/predict", file_name="ws_config.json")