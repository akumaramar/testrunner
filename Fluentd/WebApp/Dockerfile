FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["WebApp.csproj", "./"]
RUN dotnet restore "./WebApp.csproj"
COPY . .
RUN dotnet build "WebApp.csproj" -c Release -o /app/build
RUN dotnet publish "WebApp.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "WebApp.dll"]

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1
