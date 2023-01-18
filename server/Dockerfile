FROM maven:3.8.3-openjdk-17

# create project folder in container
RUN mkdir /project
# copy the whole code in that folder
COPY . /project
# navigate to that folder
WORKDIR /project
# run maven command to build jar
RUN mvn clean package -DskipTests
# launch the jar
CMD ["java", "-jar", "target/world.jar"]