using System;
using System.Threading.Tasks;
using NLog;
using NLog.Config;
using NLog.Targets;

namespace ConsoleApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var config = new LoggingConfiguration();
            
            var fluentdTarget = new NetworkTarget("fluentd")
            {
                Address = "tcp://fluentd:24224",
                Layout = "${message}"
            };
            
            config.AddTarget(fluentdTarget);
            config.AddRuleForAllLevels(fluentdTarget);
            
            LogManager.Configuration = config;
            var logger = LogManager.GetCurrentClassLogger();

            Console.WriteLine("Starting to send logs to Fluentd...");

            while (true)
            {
                try
                {
                    var logMessage = new { 
                        timestamp = DateTime.UtcNow,
                        message = $"Hello from {Environment.GetEnvironmentVariable("APP_NAME") ?? "App1"}!",
                        level = "info",
                        appName = Environment.GetEnvironmentVariable("APP_NAME") ?? "App1",
                        counter = DateTime.UtcNow.Second // Adding some varying data
                    };
                    
                    logger.Info(System.Text.Json.JsonSerializer.Serialize(logMessage));
                    Console.WriteLine("Log sent to Fluentd");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error sending log: {ex.Message}");
                }

                await Task.Delay(5000); // Wait 5 seconds before sending next log
            }
        }
    }
}
