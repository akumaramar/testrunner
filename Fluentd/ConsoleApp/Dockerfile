FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["ConsoleApp.csproj", "./"]
RUN dotnet restore "./ConsoleApp.csproj"
COPY . .
RUN dotnet build "ConsoleApp.csproj" -c Release -o /app/build
RUN dotnet publish "ConsoleApp.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime:6.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "ConsoleApp.dll"]
