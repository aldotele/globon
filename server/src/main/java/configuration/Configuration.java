package configuration;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.MapperFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.TextNode;
import io.github.cdimascio.dotenv.Dotenv;
import io.javalin.config.JavalinConfig;
import io.javalin.openapi.plugin.OpenApiPlugin;
import io.javalin.openapi.plugin.OpenApiPluginConfiguration;
import io.javalin.openapi.plugin.swagger.SwaggerConfiguration;
import io.javalin.openapi.plugin.swagger.SwaggerPlugin;
import io.javalin.plugin.bundled.CorsPluginConfig;

import java.util.function.Consumer;

public class Configuration {
    public static final ObjectMapper mapper = new ObjectMapper()
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    public static final ObjectMapper simpleMapper = new ObjectMapper()
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
            .disable(MapperFeature.USE_ANNOTATIONS);

    public static final Dotenv ENV = Dotenv.load();

    public static Consumer<JavalinConfig> appConfig = config -> {
        // openApi
        config.plugins.register(openApiPluginConfig());
        // swagger
        config.plugins.register(swaggerPluginConfig());
        // cors
        config.plugins.enableCors(cors -> cors.add(CorsPluginConfig::anyHost));
        // Get schemes annotated with @JsonScheme annotation
//        for (JsonSchemaResource generatedJsonSchema : new JsonSchemaLoader().loadGeneratedSchemes()) {
//            System.out.println(generatedJsonSchema.getName());
//            System.out.println(generatedJsonSchema.getContentAsString());
//        }
    };

    private static OpenApiPlugin openApiPluginConfig() {
        return new OpenApiPlugin(new OpenApiPluginConfiguration()
                        .withDocumentationPath("/openapi.json")
                        .withDefinitionConfiguration((version, definition) -> definition
                                .withOpenApiInfo((openApiInfo) -> {
                                    openApiInfo.setTitle("World Proxy");
                                    openApiInfo.setVersion("1.0.0");
                                })
                                .withServer((openApiServer) -> {
                                    openApiServer.setUrl(("http://localhost:7070/"));
                                    //openApiServer.setDescription("Server description goes here");
                                    //openApiServer.addVariable("port", "7070", new String[]{"7070", "8080"}, "Port of the server");
                                    //openApiServer.addVariable("basePath", "", new String[]{"", "v1"}, "Base path of the server");
                                })
                                .withDefinitionProcessor((content -> { // you can add whatever you want to this document using your favourite json api
                                    content.set("test", new TextNode("Value"));
                                    return content.toPrettyString();
                                }))
                        ));
    }

    private static SwaggerPlugin swaggerPluginConfig() {
        String deprecatedDocsPath = "/openapi.json"; // by default it's /openapi
        SwaggerConfiguration swaggerConfiguration = new SwaggerConfiguration();
        swaggerConfiguration.setDocumentationPath(deprecatedDocsPath);
        return new SwaggerPlugin(swaggerConfiguration);
    }
}

