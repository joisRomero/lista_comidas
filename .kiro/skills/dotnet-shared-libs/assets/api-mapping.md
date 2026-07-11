# ANTA.Shared.Common.Mapping API Reference

Source-based public API reference for `ANTA.Shared.Common.Mapping`.

## Table of Contents
- [Core Interfaces](#core-interfaces)
- [DI Registration](#di-registration)
- [Mapping Extensions](#mapping-extensions)
- [Converters](#converters)
- [Implementation Pattern](#implementation-pattern)

## Core Interfaces

### IMapper<TSource, TDestination> — Map(TSource) -> TDestination
Namespace: `ANTA.Shared.Common.Mapping.Abstractions`

`public interface IMapper<in TSource, out TDestination>`

`TDestination Map(TSource source);`

Creates a new destination from a source.

### IUpdater<TSource, TDestination> — Update(TSource, TDestination) -> void
Namespace: `ANTA.Shared.Common.Mapping.Abstractions`

`public interface IUpdater<in TSource, in TDestination>`

`void Update(TSource source, TDestination destination);`

Updates an existing destination with source values.

## DI Registration

Namespace: `ANTA.Shared.Common.Mapping.Extensions`

### AddAntaminaMapping(params Assembly[]) — auto-scan, registers as Singleton
`public static IServiceCollection AddAntaminaMapping(this IServiceCollection services, params Assembly[] assemblies)`

- Requires at least one assembly.
- Scans loadable concrete types.
- Registers all implemented `IMapper<,>` and `IUpdater<,>` interfaces as `ServiceLifetime.Singleton`.

### AddMapper<TMapper>(ServiceLifetime) — manual registration
`public static IServiceCollection AddMapper<TMapper>(this IServiceCollection services, ServiceLifetime lifetime = ServiceLifetime.Singleton) where TMapper : class`

- `TMapper` must implement `IMapper<,>` and/or `IUpdater<,>`.
- Registers each matching interface using the provided lifetime.

### ValidateMappingRegistrations(params Assembly[]) — fail-fast validation
`public static IServiceCollection ValidateMappingRegistrations(this IServiceCollection services, params Assembly[] assemblies)`

- Requires at least one assembly.
- Inspects public constructors for parameters typed as `IMapper<,>` or `IUpdater<,>`.
- Throws `InvalidOperationException` listing missing registrations.

## Mapping Extensions

Namespace: `ANTA.Shared.Common.Mapping.Extensions`

### MapList() — IEnumerable<TSource> -> List<TDestination>
`public static List<TDestination> MapList<TSource, TDestination>(this IMapper<TSource, TDestination> mapper, IEnumerable<TSource> source)`

- Maps each item via `mapper.Map(item)`.
- Preallocates capacity when `source` is `ICollection<TSource>`.

### MapOrDefault() — null-safe mapping
`public static TDestination? MapOrDefault<TSource, TDestination>(this IMapper<TSource, TDestination> mapper, TSource? source) where TSource : class where TDestination : class`

- Returns `null` when `source` is `null`; otherwise maps.

### UpdateList() — update destination list by index
`public static void UpdateList<TSource, TDestination>(this IUpdater<TSource, TDestination> updater, IReadOnlyList<TSource> sources, IList<TDestination> destinations)`

- Requires equal source/destination counts, else throws `ArgumentException`.
- Updates with `updater.Update(sources[i], destinations[i])`.

## Converters

Namespace: `ANTA.Shared.Common.Mapping.Converters`

### StringConverters — ToTrimmedOrNull(), Truncate()
`public static string? ToTrimmedOrNull(string? value)`

`public static string? Truncate(string? value, int maxLength)`

- `ToTrimmedOrNull`: trims and returns `null` for `null`, empty, or whitespace.
- `Truncate`: returns `null` for `null`; throws `ArgumentOutOfRangeException` when `maxLength < 0`.

### DateConverters — ToDateNumber(), FromDateNumber(), ToNullableDateTimeOffset()
`public static int ToDateNumber(DateTime date)`

`public static int? ToDateNumber(DateTime? date)`

`public static DateTime FromDateNumber(int dateNumber)`

`public static DateTime? FromDateNumber(int? dateNumber)`

`public static DateTimeOffset? ToNullableDateTimeOffset(DateTime? date)`

`public static DateTimeOffset? ToNullableDateTimeOffset(object? value)`

- `ToDateNumber`: converts `DateTime` to `YYYYMMDD`.
- `FromDateNumber`: converts `YYYYMMDD` to UTC `DateTime`.
- `ToNullableDateTimeOffset(DateTime?)`: `DateTime?` to UTC `DateTimeOffset?`.
- `ToNullableDateTimeOffset(object?)`: handles `null`, `DBNull`, `DateTime`, and `DateTimeOffset`; critical for Dapper dictionary mapping.

## Implementation Pattern

Sealed class mapper with explicit assignments:

```csharp
public sealed class SourceToDestinationMapper : IMapper<SourceModel, DestinationModel>
{
    public DestinationModel Map(SourceModel source) => new()
    {
        Id = source.Id,
        Name = source.Name
    };
}
```
