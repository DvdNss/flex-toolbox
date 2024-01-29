import com.ooyala.flex.plugins.PluginCommand
import groovy.json.JsonSlurper

class Script extends PluginCommand {
    def execute() {
        / *
        * Created on: 2024-01-29
        * By: David NAISSE
        * Main steps:
        *   - read filesHashInfo workflow variable (coming from Checksum action)
        *   - set sha1 to asset.metadata.general-info.sha1
        * Changes:
        *   -
        * /
    
        // vars
        def asset = context.asset
        def assetId = context.asset.id
        def assetMetadata = flexSdkClient.assetService.getAssetMetadata(assetId)
        def assetLocation = context.asset.fileInformation.getCurrentLocation()
        assert asset && assetId && assetMetadata && assetLocation : "Something went wrong while retrieving the asset and its metadata, possible cause: API down, asset is missing metadata. Please try again or contact Dalet support. "
    
        // retrieve sha1
        def filesHashResponse = context.getWorkflowStringVariable("filesHashInfo")
        def filesHash = new JsonSlurper().parseText(filesHashResponse).hashes
        def sha1 = filesHash.find((filename, hash) -> filename == assetLocation)
        assert filesHashResponse && sha1 : "Something went wrong while trying to read filesHashInfo workflow variable for $assetLocation. Please try again or contact Dalet support. "
    
        // output
        context.logInfo("About to set sha1 {} on assetId {}...", sha1.hash, assetId)
        assetMetadata.getField("general-info").getField("sha1").setValue(sha1.hash)
        flexSdkClient.assetService.setAssetMetadata(assetId, assetMetadata)
        context.logInfo("Successfully updated assetId {} metadata. ", assetId)
    }
}