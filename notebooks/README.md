# Notebooks Directory

This directory contains Jupyter notebooks for exploratory data analysis and model development.

## Files

- `project.ipynb` - Main project exploration and analysis
- `model_notebook.ipynb` - Model development and experimentation

## Purpose

These notebooks are used for:

- **Data Exploration**: Understanding student preferences and patterns
- **Feature Analysis**: Analyzing feature importance and correlations
- **Model Prototyping**: Testing different algorithms and approaches
- **Visualization**: Creating charts and graphs for insights
- **Experimentation**: Trying new ideas before production implementation

## Running Notebooks

```bash
# Install Jupyter if not already installed
pip install jupyter

# Start Jupyter server
jupyter notebook

# Navigate to notebooks/ directory and open desired notebook
```

## Notebook Contents

### project.ipynb
- Data loading and initial exploration
- Statistical analysis of student features
- Visualization of distributions and correlations
- Preliminary clustering analysis

### model_notebook.ipynb
- Model training experiments
- Hyperparameter tuning
- Performance evaluation
- Comparison of different approaches

## Best Practices

- Keep notebooks organized with clear sections
- Document your findings and insights
- Export important visualizations
- Clean up experimental code before committing
- Use markdown cells for explanations

## Converting to Scripts

To convert a notebook to a Python script:

```bash
jupyter nbconvert --to script notebook_name.ipynb
```
