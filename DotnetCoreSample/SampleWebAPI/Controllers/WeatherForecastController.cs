using App.Metrics.Formatters.Prometheus;
using Microsoft.AspNetCore.Mvc;
using Prometheus;
using System.Diagnostics;
using Counter = Prometheus.Counter;
using Histogram = Prometheus.Histogram;

namespace SampleWebAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

        private readonly ILogger<WeatherForecastController> _logger;
        private static readonly Counter ProcessedJobCount = Metrics.CreateCounter("dotnet_request_operations_total", "The total number of processed requests");
        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet(Name = "GetWeatherForecast")]
        public IEnumerable<WeatherForecast> Get()
        {
            var sw = Stopwatch.StartNew();

            sw.Stop();
            ProcessedJobCount.Inc();
            var histogram = 
            Metrics.CreateHistogram("dotnet_request_duration_seconds", "Histogram for the duration in seconds",
                                    new HistogramConfiguration{
                                        Buckets = Histogram.LinearBuckets(start:1,width: 1,count:5) });

            histogram.Observe(sw.Elapsed.TotalSeconds);
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = Random.Shared.Next(-20, 55),
                Summary = Summaries[Random.Shared.Next(Summaries.Length)]
            })
            .ToArray();
        }
    }
}