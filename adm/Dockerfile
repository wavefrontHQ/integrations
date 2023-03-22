FROM openjdk:8u111-alpine
WORKDIR /
ADD ./target/query-service-0.0.1-SNAPSHOT.jar query-service.jar
EXPOSE 8080
CMD java -jar query-service.jar
