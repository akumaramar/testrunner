using NLog;
using NLog.Config;
using NLog.Targets;
using NLog.Web;

var builder = WebApplication.CreateBuilder(args);

// Configure NLog
var config = new LoggingConfiguration();
var fluentdTarget = new NetworkTarget("fluentd")
{
    Address = "tcp://fluentd:24224",
    Layout = "${message}"
};

config.AddTarget(fluentdTarget);
config.AddRuleForAllLevels(fluentdTarget);
LogManager.Configuration = config;

// Add services to the container
builder.Host.UseNLog();
var logger = LogManager.GetCurrentClassLogger();

var app = builder.Build();

// Middleware to log all requests
app.Use(async (context, next) =>
{
    var logMessage = new
    {
        timestamp = DateTime.UtcNow,
        message = $"Request to {context.Request.Path}",
        level = "info",
        appName = Environment.GetEnvironmentVariable("APP_NAME") ?? "WebApp",
        path = context.Request.Path.ToString(),
        method = context.Request.Method,
        userAgent = context.Request.Headers.UserAgent.ToString()
    };
    logger.Info(System.Text.Json.JsonSerializer.Serialize(logMessage));
    await next();
});

// Example endpoints that generate different types of logs
app.MapGet("/", () =>
{
    var logMessage = new
    {
        timestamp = DateTime.UtcNow,
        message = "Homepage accessed",
        level = "info",
        appName = Environment.GetEnvironmentVariable("APP_NAME") ?? "WebApp",
        endpoint = "/"
    };
    logger.Info(System.Text.Json.JsonSerializer.Serialize(logMessage));
    return "Welcome to the logging demo!";
});

app.MapGet("/error", () =>
{
    var logMessage = new
    {
        timestamp = DateTime.UtcNow,
        message = "Simulated error occurred",
        level = "error",
        appName = Environment.GetEnvironmentVariable("APP_NAME") ?? "WebApp",
        endpoint = "/error",
        errorCode = "SIMERR001"
    };
    logger.Error(System.Text.Json.JsonSerializer.Serialize(logMessage));
    return "Simulated error logged!";
});

app.MapGet("/warning", () =>
{
    var logMessage = new
    {
        timestamp = DateTime.UtcNow,
        message = "System running low on resources",
        level = "warning",
        appName = Environment.GetEnvironmentVariable("APP_NAME") ?? "WebApp",
        endpoint = "/warning",
        memoryUsage = "85%"
    };
    logger.Warn(System.Text.Json.JsonSerializer.Serialize(logMessage));
    return "Warning logged!";
});

// Health check endpoint
app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));

app.Run("http://0.0.0.0:80");
