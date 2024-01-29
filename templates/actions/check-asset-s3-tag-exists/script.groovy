import com.ooyala.flex.plugins.PluginCommand
import com.amazonaws.auth.AWSStaticCredentialsProvider
import com.amazonaws.auth.BasicAWSCredentials
import com.amazonaws.services.s3.AmazonS3ClientBuilder
import com.amazonaws.services.s3.model.GetObjectTaggingRequest

class Script extends PluginCommand {
    def execute() {
        / *
        * Created on: 2024-01-29
        * By: David NAISSE
        * Main steps:
        *   - Build s3 client
        *   - Get sha1 s3 tag
        *   - Return TRUE if sha1 tag exists, else FALSE
        * Changes:
        *   - 
        * /
    
        // vars
        def AWS_KEY = "@[Wb-S3-key]"
        def AWS_SECRET = "@[Wb-S3-secret]"
        def AWS_TAGS = ["computed-sha1", "sha1"]
        def assetId = context.asset.id
        def assetLocation = context.asset.fileInformation.getCurrentLocation()
        def assetBucket = assetLocation.split('/')[2]
        def assetPath = assetLocation.replace("s3://$assetBucket/", "")
        assert assetLocation && assetBucket && assetPath : "Something went wrong while retrieving the asset information. Please try again or contact Dalet support. "
    
        // s3 client
        def s3Client = AmazonS3ClientBuilder.standard()
                .withCredentials(
                        new AWSStaticCredentialsProvider(
                                new BasicAWSCredentials(AWS_KEY, AWS_SECRET)
                        )
                )
                .build()
    
        // get s3 tag sha1
        def assetTagRequest = new GetObjectTaggingRequest(assetBucket, assetPath)
        def assetTags = s3Client.getObjectTagging(assetTagRequest).getTagSet()
        def sha1Tag = assetTags.find() { tag -> tag.key in AWS_TAGS }
    
        // output
        if (sha1Tag) {
            context.logInfo("Found one of {} s3 tag {} for asset {}.", AWS_TAGS as String, sha1Tag.value, assetId)
            return "TRUE"
        } else {
            context.logInfo("Cannot find one of {} s3 tag for asset {}.", AWS_TAGS as String, assetId)
            return "FALSE"
        }
    }
}