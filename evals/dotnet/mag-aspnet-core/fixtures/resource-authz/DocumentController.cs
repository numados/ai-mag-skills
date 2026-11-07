using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Fixture.Documents;

[ApiController]
[Route("documents")]
[Authorize]
public sealed class DocumentController : ControllerBase
{
    // Defect: access must depend on the loaded document's Owner, but
    // [Authorize] evaluates before the document is loaded and cannot inspect
    // its contents. This only guarantees the user is authenticated, not that
    // they own the document.
    [HttpGet("{id}")]
    public async Task<ActionResult<Document>> Get(int id)
    {
        var document = await LoadDocumentAsync(id);
        if (document is null)
        {
            return NotFound();
        }

        return Ok(document);
    }

    private static Task<Document?> LoadDocumentAsync(int id) =>
        Task.FromResult<Document?>(new Document(id, "alice"));
}

public sealed record Document(int Id, string Owner);
