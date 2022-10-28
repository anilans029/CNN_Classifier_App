# Classifier App

## Developmemt workflow

1. Update config.yaml
3. Update params.yaml
2. Update secrets.yaml [optional]
4. Update the entity
5. Update the configuration in src/config
6. Update the components
7. Update the pipeline
8. Test run pipeline stage
9. Run tox for testing the package
10. Update the dvc.yaml
11. run "dvc repo" for running all the stages in the pipeline

![img](docs\project_workflow.png)

## setup
1. To create the project structure
```
python template.py
```
2. initialize the setup (use in git bash terminal)
```
bash init_setup.sh
```
