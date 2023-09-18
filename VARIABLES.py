"""

    PROJECT: flex_toolbox
    FILENAME: VARIABLES.py
    AUTHOR: David NAISSE
    DATE: September 11, 2023

    DESCRIPTION: variables file

"""
from enum import Enum

ACTION_CONFIG = {
    "accountId": 0,
    "allowedAutoRetryAttempts": "",
    "autoRetryInterval": "",
    "concurrentJobsLimit": 0,
    "description": "",
    # "externalIds": [
    #     {}
    # ],
    "name": "",
    "pluginClass": "",
    "pluginUuid": "",
    "priority": "",
    # "redoActionId": -1,
    "runRuleExpression": "",
    "supportsAutoRetry": False,
    "timeout": 0,
    "type": "",
    # "undoActionId": -1,
    "useLatestAvailableVersion": True,
    "visibilityIds": [
        0
    ]
}

WORKFLOW_CONFIG = {
    "accountId": 0,
    "concurrentWorkflowLimit": 0,
    "description": "string",
    "name": "string",
    "visibilityIds": [
        0
    ]
}

DEFAULT_GROOVY_SCRIPT = "import com.ooyala.flex.plugins.PluginCommand\n\nclass script extends PluginCommand {\n\tdef execute(){\n\t\t// your code here\n\t}\n}"

FLEX_ITEMS = ['accounts', 'actions', 'assets', 'collections', 'eventHandlers', 'events', 'groups', 'jobs',
              'messageTemplates', 'metadataDefinitions', 'objectTypes', 'profiles', 'quotas', 'resources', 'roles',
              'tags', 'taskDefinitions', 'tasks', 'taxonomies', 'taxonomies', 'timedActions', 'userDefinedObjectsTypes',
              'users', 'variants', 'variants', 'wizards', 'workflowDefinitions', 'workflows', 'workspaces']


class PluginType(Enum):
    """ Enum of plugin types. """
    addToGroup: str = "Add to Group"
    addToIMP: str = "Add to IMP"
    analyze: str = "Analyze"
    archive: str = "Archive"
    cancel: str = "Cancel"
    checksum: str = "Checksum"
    copy: str = "Copy"
    createObject: str = "Create Object"
    createProxy: str = "Create Proxy"
    decision: str = "Decision"
    delete: str = "Delete"
    deleteArchive: str = "Delete Archive"
    deliver: str = "Deliver"
    export: str = "Export"
    extract: str = "Extract"
    importObject: str = "Import"
    ingest: str = "Ingest"
    launch: str = "Launch"
    message: str = "Message"
    modifyRelationship: str = "Modify Relationship"
    move: str = "Move"
    permission: str = "Permission"
    publish: str = "Publish"
    publishPlayer: str = "Publish Player"
    purge: str = "Purge"
    qualityControl: str = "Quality Control"
    reImport: str = "ReImport"
    rename: str = "Rename"
    rePublish: str = "Republish"
    rePublishPlayer: str = "Republish Player"
    restore: str = "Restore"
    restoreArchive: str = "Restore Archive"
    script: str = "Script"
    setMetaDef: str = "Set Meta. Def"
    setMetadata: str = "Set Metadata"
    startSession: str = "Start Session"
    stopSession: str = "Stop Session"
    touch: str = "Touch"
    transcode: str = "Transcode"
    unarchive: str = "Unarchive"
    unpublish: str = "Unpublish"
    unpublishPlayer: str = "Unpublish Player"
    validate: str = "Validate"
    wait: str = "Wait"
