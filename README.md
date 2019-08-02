# Data Driven Research-Paper
![img](ddrp-icon-shadow.png)

(In Python and Latex)


## What this is:

## What this is not:

## How to use this repository

### Conda Environment
Have Anaconda installed (recommend Miniconda) and accessible via PATH (`conda` should work in your terminal). These instructions assume `conda>=4.6`. Rather than install each package as you need it it *directly*, we are going to be using an environment YAML file to keep track of all major dependencies you rely on. This will help you and others recreate the environment in the future.

To start, open the `environment.yml` file in the top-lvl directory. 

1. **Rename your environment**. 
This name will be used for all activation/deactivation in terminal and PyCharm, e.g. 
    `conda activate my-project-envname` 
before working, and `conda deactivate` after you're done. 
    
2. **Set environment channels** 
Usually the two supplied should be fine, as `conda` is the most typical, with many cutting-edge or latest-release packages can use `conda-forge`. If any packages you wish to install use a `-c some-channel` flag in the installation instructions, add `some-channel` here and it will automatically be searched during installation. 

3. **Conda Dependencies** 
Any packages that support conda installation can be added here as a member of the list. Some defaults have been provided, including `jupyter` which allows you to use notebooks, along with any `ipython` features, by extension. *NOTE*: versioning is done with the `conda` [package match specifications](https://docs.conda.io/projects/conda-build/en/latest/resources/package-spec.html#package-match-specifications)

4. **Pypi Dependencies** 
By far the most common way to install a package is via pip. The reason we are not using `pipenv` or `virtualenv` is that `conda` supports direct installation of Pypi packages, using a `pip` sublist. This supports names, version globbing, and even direct repository installation for unreleased packages e.g: 
```yaml
dependencies:
  - python=3.7
  - pip    
  - pip:
      - statsmodels
      - git+https://github.com/networkx/networkx.git
      - pomegranate==0.11.*
```

5. Creating/Maintaining
To create the environment (prior to activating it) simply run `conda env create -f environment.yml`. Then, if a new package is needed, rather than directly installing it via terminal, add it to the environment file and update your environment directly: `conda env update -f environment.yml`

### LaTeX Submodule
It is likely your latex files are already versioned---likely via git. This is because *all overleaf documents are git-versioned*. This is largely why this repository exists. This is where `git submodule` comes in!


- (in overleaf) menu > sync (git) > copy/paste url
- (in top-level directory) `git submodule add path_to_repo`
- `git mv ugly_number_name latex/submod_name`
- `git commit -am ‘added latex to code repo or something’

From now-on, be *very careful* of adding/commiting, etc. It's **always** a good idea to try out `git status` in your main repo before pushing a lot, but you should also get in the habit of doing it in the submodule, too. As you add images/figures/tables/etc. to your submodule from the rest of this repo (likely the `utils` scripts), you will need to pull/add/commit/push *in that order* from within the submodule directory. Then do the same for the top-level. 

TODO: Make a script to automate this, from the top-lvl dir. 
 