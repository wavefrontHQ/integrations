package com.github.jhuynh1.geode.wavefront;

import io.micrometer.core.instrument.Clock;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.wavefront.WavefrontConfig;
import io.micrometer.wavefront.WavefrontMeterRegistry;
import org.apache.geode.metrics.MetricsPublishingService;
import org.apache.geode.metrics.MetricsSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GeodeWavefrontPublisher implements MetricsPublishingService {
    final static Logger logger = LoggerFactory.getLogger(GeodeWavefrontPublisher.class);
    private volatile MeterRegistry registry;

    @Override
    public void start(MetricsSession session) {
        logger.info("Starting geode-wavefront-publisher");
        registry = createWavefrontRegistry();

        // add the Wavefront registry as a sub-registry to the cache's composite registry
        session.addSubregistry(registry);
    }

    @Override
    public void stop(MetricsSession session) {
        logger.info("Stopping geode-wavefront-publisher");
        session.removeSubregistry(registry);
    }

    private MeterRegistry createWavefrontRegistry() {
        WavefrontConfig config = new WavefrontConfig() {
            private final String prefix = System.getProperty("geode-wavefront-prefix", "wavefront.geode");
            private final String apiToken = System.getProperty("geode-wavefront-api-token");
            private final String source = System.getProperty("geode-wavefront-source", "apache.geode");
            @Override
            public String uri() {
                return "https://vmware.wavefront.com";
            }

            @Override
            public String apiToken() {
                //This is the key you can generate from your Wavefront account
                return apiToken;
            }

            @Override
            public String get(String key) {
                //Accept rest of Wavefront defaults by returning null
                return null;
            }

            @Override
            public String prefix() {
                return prefix;
            }

            @Override
            public String source() {
                return source;
            }
        };
        return new WavefrontMeterRegistry(config, Clock.SYSTEM);
    }
}