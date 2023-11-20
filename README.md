#### Requirements

- Python 3.9

#### Commands

* add environment to config
  ```shell
  ftbx connect "https://devstaging.flex.daletdemos.com" username password
  ```

* connect to a known environment (must be in `environments.json`)
  ```shell
  # Full URL
  ftbx connect "https://devstaging.flex.daletdemos.com"
  
  # Partial URL
  ftbx connect "daletdemos.com"
  ftbx connect "devstaging.flex"
  
  # Alias
  ftbx connect "dalet-sandbox"
  ```
  
  ```shell
  # Output
  Successfully connected to https://portal.dev.archive.warnerbros.com - this environment is now your default environment.
  ```
* show default env
  ```shell
  ftbx env
  ```
  
  ```shell
  # Output
  Current default environment is https://portal.dev.archive.warnerbros.com - user: dnaisse.
  ```
  
* query anything
  ```shell
  # GET
  ftbx query GET actions/410 # same as below
  ftbx query GET https://master.cs-sandbox.flex.cs.dalet.cloud/api/actions/410
  
  # POST/PUT
  ftbx query PUT actions/410/configuration --payload payload.json
  ```
  
  ```shell
  # Output
  Performing [GET] https://portal.dev.archive.warnerbros.com/api/actions/28938...

  Result of the query has been saved in query.json for your best convenience. 
  ```

* list config items (workflowDefinitions, actions..) and their ids
  ```shell
  # List actions and their ids
  ftbx list actions

  # List assets with fql
  ftbx list assets --filters "fql=(mimetype~mp4)"
  
  # List 5 jobs in a failed status
  ftbx list jobs --filters status=Failed limit=5
  
  # List script that contains "createJob"
  ftbx list actions --filters "type=script" --post_filters "configuration.instance.script-contents.script~createJob"
  
  # List actions with concurrency > 0
  ftbx list actions --post_filters "concurrencyJobsLimit>0"
  ```
  
  ```shell
  # Output
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

* pull items
  ```shell
  # Pull **ALL** actions from default env
  ftbx pull actions
  
  # Pull default env actions matching a filter (several filters can be selected)
  ftbx pull actions --filters name=action_name
  ftbx pull actions --filters id=309
  ftbx pull actions --filters enabled=true
  ftbx pull actions --filters type=script
  ftbx pull actions --filters type=script enabled=true
  
  # Pull **ALL** from default env
  ftbx pull all
  
  # Pull all default env actions without deps
  ftbx pull actions --with_dependencies false
  
  # Pull actions where script contains "context.asset.id"
  ftbx pull actions --post_filters "configuration.instance.script-contents.script~context.asset.id" 
  
  # Pull workflows (variables and jobs come by default)
  ftbx pull workflows --filters "id=978324"
  
  # Pull workflows without vars and jobs
  ftbx pull workflows --filters "id=978324" "includeVariables=false" "includeJobs=false"
  
  # Pull actions from several envs at the same time
  ftbx pull actions --envs "wb-dev" "wb-stg" "wb-prod" --filters "name=set-asset-metadata"
  ```
  
* push items
  ```shell
  # Push action to an env (will be created if doesn't exist)
  ftbx push actions check-end-node-wf 
  
  # Push job
  ftbx push jobs 294036
  
  # push action to failed jobs and retry them
  ftbx push actions check-end-node-wf --push_to_failed_jobs true
  ```
  
* restore backup (in config_item/item_name/backup)
  ```shell
  ftbx restore actions set-tech-metadata-dpx "2023-10-10 15h53m43s"
  ```
  
* compare items
  ```shell
  ftbx compare actions wb-dev wb-stg wb-prod --filters name=set-tech-metadata-dpx
  ```
  
  ```shell
  # Output
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