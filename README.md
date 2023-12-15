# __Requirements__

#### [Python 3.9 (click here to download)](https://www.python.org/downloads/release/python-390/)

***

# __Installation__

## 1. Windows

* install Python (link above)  

* clone the repo, install requirements and run ftbx init    

```shell
git clone git@bitbucket.org:ooyalaflex/flex-toolbox.git
cd flex_toolbox
pip install -r requirements.txt
ftbx init
```

* add ftbx to your environment variables  
  
1. Windows Menu  
2. Edit the system environment variables  
3. Environments variables  
4. User variables > Path  
5. Add path to flex toolbox (ex: C:\Users\dvdna\PyCharmProjects\flex_toolbox)  

* If you want to be able to render workflow graphs as PNG, please download [GraphViz](https://www.graphviz.org/), add it
  to your PATH environment variable and update `VARIABLES.py` as follows:

```python
# Params
RENDER_WORKFLOW_GRAPHS = True
```

You will then be able to use the `ftbx` command anywhere in windows with the options below.

***

## 2. Linux

* install Python (link above)  

* clone the repo, install requirements and run ftbx init  

```shell
git clone git@bitbucket.org:ooyalaflex/flex-toolbox.git
cd flex_toolbox
pip install -r requirements.txt
ftbx init
```

* If you want to be able to render workflow graphs as PNG, please download [GraphViz](https://www.graphviz.org/), add it
  to your PATH environment variable and update `VARIABLES.py` as follows:

```python
# Params
RENDER_WORKFLOW_GRAPHS = True
```

You will then be able to use the `ftbx` command anywhere in windows with the options below.


* add ftbx to your aliases
```shell
# in ~/.bashr
alias ftbx="path\to\flex_toolbox"
```

***

# __Commands__

## __Connection/Setup__

This command does 3 things:  
  
- add environment credentials to your environments.json  
- check connection against the env with url, username and password  
- set the environment as your default environment if connection successfull  

```shell
# MAIN COMMAND
ftbx connect <env_url_or_alias> <username> <password>
```

> options:  
> --alias [String]: alias to set for the environment (ex: wb-stg for warner brother STG)

---

#### 1. Connect to a new environment

```shell
ftbx connect "https://devstaging.flex.daletdemos.com" "username" "password"
```

> Note: this will save the env configuration in `environments.json`, set the env as your default environment, and ping
> the env to check its connection.  

---

#### 2. Connect to a known environment (must be in `environments.json`)

```shell
# environments.json:
# "dalet-sandbox": {
#     "url": "https://devstaging.flex.daletdemos.com",
#     "username": "xxx",
#     "password": "xxx"
# }

# Full URL
ftbx connect "https://devstaging.flex.daletdemos.com"

# Partial URL
ftbx connect "daletdemos.com"
ftbx connect "devstaging.flex"

# Alias
ftbx connect "dalet-sandbox"
```

---

#### 3. Display default environment

```shell
ftbx env
```

## __Raw Queries__

This command queries any env without the need of setting up headers etc..

```shell
# MAIN COMMAND
ftbx query <method> <long_or_short_query>
```

> options:  
> --env [String] environment to query if not default environment  
> --payload [String] path to payload (JSON) file  

---

#### 1. Query absolutely everything

```shell
# GET (commands below are the same)

# Default env
ftbx query GET "actions/410"
# Full url
ftbx query GET "https://master.cs-sandbox.flex.cs.dalet.cloud/api/actions/410"
# Env alias (can be partial too)
ftbx query GET "actions/410" --env "cs-sbx"

# POST/PUT (same args as above, plus --payload)
ftbx query PUT "actions/410/configuration" --payload "payload.json"
```

## __List items__

This command queries any env and displays the main info of the requested items, as well as the requested post_filters
values. Two files will then be created:  

- a list.csv file with a dataframe (excel sheet)  
- a list.json file with the raw result of the request  

```shell
ftbx list <config_item>
```

> options:  
> --env [String]: environment to query if not default environment  
> --filters [String(s)]: filters to apply, that are used directly within the query  
> --post_filters [String(s)]: post retrieval filters, that are applied after query (operators: '!=', '>=', '<=', '~', '=', '<', '>')  

---

#### 1. List anything

  ```shell
  # List all actions 
  ftbx list actions # default env
  ftbx list actions --env "wb-prod"

  # List all assets with fql
  ftbx list assets --filters "fql=(mimetype~mp4)" # default env
  ftbx list assets --filters "fql=(mimetype~mp4)" --from "wb-prod"
  
  # List 5 jobs in a failed status 
  ftbx list jobs --filters "status=Failed" "limit=5" # default env
  ftbx list jobs --filters "status=Failed" "limit=5" --from "wb-prod"
  
  # List scripts that contains "createJob"
  ftbx list actions --filters "type=script" --post_filters "configuration.instance.script-contents.script~createJob"
  ftbx list actions --from "wb-prod" --filters "type=script" --post_filters "configuration.instance.script-contents.script~createJob"
  
  # List all actions with concurrency > 0 from default env
  ftbx list actions --post_filters "concurrencyJobsLimit>0" # default env
  ftbx list actions --post_filters "concurrencyJobsLimit>0" --from "wb-prod"
  ```
  
  ```shell
  # OUTPUT
  Performing [GET] https://portal.dev.archive.warnerbros.com/api/actions;type=script;limit=10...

  Retrieving actions: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.46it/s]
  Retrieving actions []: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<?, ?it/s]

                     name                   id    type.name                       pluginClass
  1          action-modified-test-script  1874308   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  2    create-placeholder-sequence-group  1856453   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  3   delete-asset-from-bm-event-handler  1856600   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  4                   prepare-delete-udo  2026696   script    tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand
  5                 sc-create-collection  1863345   script    tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand
  6                sc-sharing-collection  1863346   script    tv.nativ.mio.plugins.actions.jef.JEFActionProxyCommand
  7                                 test  2338482   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  8                update-gatorsky-to-in  1856601   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  9                   wamo-purge-trigger  1917236   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand
  10                 wamo-query-aws-sign  1837898   script   tv.nativ.mio.plugins.actions.script.GroovyScriptCommand

  Results of the query have been saved as list.json for your best convenience.
  ```

## __Pull items__

This command queries any env and locally creates folders/files for the requested items. Structure will be in the following format:  

- `<config_item>/`  
    - `<item_name>/`  
        - `_object.json`: main config of the item  
        - `<item_property>.json`: item properties (ex: configuration, variables..)  

```shell
ftbx pull <config_item>
```

> options:  
> --from [String(s)]: environments to pull from if not default environment  
> --filters [String(s)]: filters to apply, that are used directly within the query  
> --with_dependencies [Boolean - default:False]: whether to retrieve all the items dependencies (ex: workflows of launch actions etc..)  
> --post_filters [String(s)]: post retrieval filters, that are applied after query (operators: '!=', '>=', '<=', '~', '=', '<', '>')  

---

#### 1. Pull anything

```shell
# Pull **ALL** actions
ftbx pull actions # default env
ftbx pull actions --from "wb-stg"

# Pull actions matching filters
ftbx pull actions --filters "name=set-asset-metadata" --from "wb-stg"
ftbx pull actions --filters "id=309" # default env
ftbx pull actions --filters "enabled=true" # default env
ftbx pull actions --filters "type=script" --from "wb-stg"
ftbx pull actions --filters "type=script" "enabled=true" # default env

# Pull **ALL**
ftbx pull all
ftbx pull all --from "wb-stg"

# Pull env actions without deps
ftbx pull actions --with_dependencies "false" # default env

# Pull all actions where script contains "context.asset.id"
ftbx pull actions --post_filters "configuration.instance[text]~destPath"

# Pull workflows (workflow variables and jobs come by default)
ftbx pull workflows --filters "id=978324"

# Pull workflows without vars and jobs
ftbx pull workflows --filters "id=978324" "includeVariables=false" "includeJobs=false"

# Pull actions from several envs at the same time
ftbx pull actions --from "wb-dev" "wb-stg" "wb-prod" --filters "name=set-asset-metadata"
```

## __Push items__

This command pushes local items to the destination environments. Process is as shown below:  

1. check if item exists locally  
   - yes: continue  
   - no: stop  
2. check if item exists in the destination environment  
   - yes: pull to `<item_name>/backup/` in case you break something  
   - no: create it in destination environment  
3. push updated item properties (ex: configuration.json, script.groovy etc..)  
4. pull updated items from the destination environment for verification purposes  

```shell
ftbx push <config_item> <item_name>
```

> options:  
> --from [String] environment to push from if not default environment  
> --to [String(s)] environments (yes, several at the same time is possible) to push to if not default environment  
> --push_to_failed_jobs [Boolean - default:False] whether to update and restart failed jobs if item is an action  

---

#### 1. Push anything

```shell
# Push action to an env
ftbx push actions check-end-node-wf # from default env to default env

# Push job (yes, you can pull jobs directly and tweak their code in your IDE)
ftbx push jobs 294036 # from default env to default env

# Push updated action to failed jobs and retry them
ftbx push actions "check-end-node-wf" --push_to_failed_jobs "true"

# Push action from wb-dev to wb-stg AND wb-prod (yes)
ftbx push actions "set-asset-metadata" --from "wb-dev" --to "wb-stg" "wb-prod""
```

## __Restore items__

This command restores an item from a backup (every push generates a backup) in case you break something.

```shell
ftbx restore <config_item> <item_name> <timestamp_or_backup_name>
```

---

#### 1. Restore backup (in config_item/item_name/backup)

```shell
ftbx restore actions set-tech-metadata-dpx "2023-10-10 15h53m43s"
```
<<<<<<< HEAD
  
## __Compare items__
=======

## Compare items
>>>>>>> 79d9f6b (added retry feature (tested), updated README.md)

This command compares items from different environments. The first environment provided in the list is always the reference environment. The list of differences will then be saved in a `compare/` folder with a TSV file for each item (no file if no differences).  

- **'x'** means same value as reference environment  
- **'NaN'** means value is missing in comparand  
- **'/!\\'** means value is different than reference environment  

```shell
ftbx compare <config_item> <list_of_envs>
```

> options:  
> --filters [String(s)]: filters to apply, that are used directly within the query  

---

#### 1. Compare items

```shell
ftbx compare actions "wb-dev" "wb-stg" "wb-prod" --filters "name=check-end-node-wf"
```

```shell
# OUTPUT
Performing [GET] https://portal.dev.archive.warnerbros.com/api/actions;name=check-end-node-wf...

Retrieving actions: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.43it/s]
Retrieving actions ['configuration']: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.70it/s]
  
Performing [GET] https://vault.stg.archive.warnerbros.com/api/actions;name=check-end-node-wf...
  
Retrieving actions: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.12it/s]
Retrieving actions ['configuration']: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.58it/s] 
  
Performing [GET] https://vault.archive.warnerbros.com/api/actions;name=check-end-node-wf...
  
Retrieving actions: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.72it/s]
Retrieving actions ['configuration']: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.89it/s] 
  
                                                      wb-dev            wb-stg wb-prod
name                                                  check-end-node-wf     x       x
displayName                                           check-end-node-wf     x       x
description                                                               NaN       x
enabled                                                            True     x       x
type.name                                                      decision     x       x
type.displayName                                               Decision     x       x
type.category                                                  Workflow     x       x
pluginClass                                ScriptedMultiDecisionCommand     x       x
pluginVersion                                                     1.0.0     x     NaN
latestPluginVersion                                               1.0.0     x     NaN
useLatestAvailableVersion                                          True     x     NaN
runRuleExpression                                                         NaN       x
supportsAutoRetry                                                 False     x       x
concurrentJobsLimit                                                   0     x       x
configuration.instance.script_type.script                        <CODE>   /!\     /!\

```

## Retry items

This command bulk retries job/workflow instances within a Flex environment, either from a query or from JSON/CSV files.  

```shell
ftbx retry <config_item> <options>
```

> options:  
> --filters [String(s)]: filters to apply, that are used directly within the query  
> --from [String]: environment alias if not default  
> --file [String]: JSON or CSV file to take as input  

* CSV format:  
CSV file must contain at least the "id" column, the number/name/order of the other columns doesn't matter.  

| id  | other_column_name | other_column_status |
|-----|-------------------|---------------------|
| 238 | job1              | Failed              |
| 239 | job2              | Failed              |
| 240 | job3              | Failed              |

* JSON format:  
JSON file must contain a dict with an "id" key for each instance, the number/name/order of the other keys doesn't matter.  

```json
{
  "workflow_1": {"id": 238, "other_key_1": "..."},
  "workflow_2": {"id": 239, "other_key_1": "..."},
  "workflow_3": {"id": 240, "other_key_1": "..."},
  ...
}
```

---

### 1. Retry instances

```shell
# retry 5 failed "untar-frames" jobs with query
ftbx retry jobs --filters "name=untar-frames" "limit=5"

# retry all failed "untar-frames" jobs
ftbx retry jobs --filters "name=untar-frames"

# retry **ALL** failed jobs/workflows
ftbx retry jobs
ftbx retry workflows

# retry all failed jobs from a CSV file (CSV file must contain the "id" column)
ftbx retry jobs --file "failed_jobs.csv"

# retry all failed workflows from a JSON file (JSON file must be made of a dict for each instance, with a "id" key within each dict)
ftbx retry workflows --file "failed_workflows.json"

# LIST + RETRY flow
ftbx list jobs --filters "status=Failed" "name=untar-frames" # this will create a JSON and CSV file with the failed items 
ftbx retry jobs --file "list.json" # same as below
ftbx retry jobs --file "list.csv" # same as above
```
