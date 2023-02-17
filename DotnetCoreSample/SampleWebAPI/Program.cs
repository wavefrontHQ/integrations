// Weather Forecast Sample Application
using Prometheus;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddMetrics();
builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.UseHttpMetrics();
app.UseAuthorization();
app.UseMetricServer();
app.UseHttpMetrics();
//app.UseMetricsWebTracking()
//            .UseMetrics(options =>
//            {
//                options.EndpointOptions = endpointsOptions =>
//                {
//                    endpointsOptions.MetricsTextEndpointOutputFormatter = new MetricsPrometheusTextOutputFormatter();
//                    endpointsOptions.MetricsEndpointOutputFormatter = new MetricsPrometheusProtobufOutputFormatter();
//                    endpointsOptions.MetricsEndpointEnabled = false;
//                };
//            });
app.MapControllers();

app.Run();
