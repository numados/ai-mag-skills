# SDK container publishing

Read when producing a container image from a .NET project via the SDK (no Dockerfile), or verifying an existing container publish setup. Scope stays local and reversible; registry push and deployment are separate, explicitly-authorized steps.

## Local and reversible by default

`dotnet publish /t:PublishContainer` (the SDK container targets) builds the app and creates an Open Container Initiative (OCI) image. It does not need Docker to build the image, and by default it pushes to the local container runtime (Docker or Podman), not to a remote registry.

Prefer the most reversible artifact for diagnosis or handoff: export to a tarball with

```
dotnet publish --os linux --arch x64 /t:PublishContainer -p ContainerArchiveOutputPath=./images/app.tar.gz
```

This needs no running container daemon and produces a file that can be scanned, stored, or loaded locally (`docker load` / `podman load`). Building to the local daemon is acceptable when the user has a runtime and asked for a runnable image.

## Registry push is a separate, authorized step

A remote push happens only when `ContainerRegistry` is set (for example `-p ContainerRegistry=ghcr.io`) or a publish profile targets a registry. Do not add that property, write a deploy profile, or run a push unless the user explicitly requested it. Keep "build an image" and "publish to a registry" as distinct outputs in any plan.

## Properties to check or set

- `ContainerRepository` — image repository/name; defaults to `AssemblyName`, which may not be a valid image name.
- `ContainerArchiveOutputPath` — tarball output (reversible, no daemon required).
- `ContainerRegistry` — only when a remote push is authorized.
- `--os` / `--arch` — target operating system and architecture (RID).

Verify the base image, target RID, entrypoint, and exposed ports against the app's runtime needs before declaring success; an image that builds but will not start is not verified. The full property list lives in the official containerization documentation, not here.

## Constraints

- SDK container support is version-dependent: the `dotnet publish` container tutorial requires the .NET 8+ SDK, and the underlying `Microsoft.NET.Build.Containers` targets must be present in the selected SDK. Check the installed SDK before assuming the targets exist.
- A missing or misconfigured container runtime surfaces only at the image-creation or load step, not during compile.
- Trimming, AOT, and single-file settings interact with the base image and entrypoint; cross-check `aot-trimming.md` when they are enabled together.

## Official references

- Containerize a .NET app with dotnet publish: https://learn.microsoft.com/en-us/dotnet/core/docker/publish-as-container
