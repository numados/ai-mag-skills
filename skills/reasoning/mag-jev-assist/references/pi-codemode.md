# Pi codemode adapter

Use only when Pi codemode and a permitted Jev classifier are available. Consult the environment's current `codemode` documentation if its API differs. `searchTools()` ranks tool descriptions; `describeTool()` supplies the declaration. Neither establishes that a tool is accessible or suitable.

## Prerequisites

This is an integration example, not a Jev installer. The host must expose codemode's model API. Its provider configuration must already supply Jev access and any required credentials. This catalog does not distribute a classifier runtime or define a universal provisioning command.

For a setup request, establish the user's actual host and provider. Then consult their supported configuration documentation. Do not guess an endpoint or ask the user to paste credentials into chat. If no permitted Jev classifier is available, use ordinary reasoning or tools instead. Report the limitation if it affects the task. The rest of the catalog does not require Jev.

## Classification example

The example is a bounded relevance decision, not a generic prompt for unrestricted reasoning. Replace the synthetic state and criteria with the minimum permitted task context:

```js
const available = await models.getAvailableOfType("classifier");
// Choose only an available Jev provider permitted for this data and task.
const jev = available.find(m => /(^|\/)jev(?:-|$)/i.test(m.id));
if (!jev) return { status: "unavailable" };
const result = await models.classify(jev, {
  state: { question: "Does the report discuss refunds?", excerpt: "Refunds are issued within five days." },
  questions: {
    relevance: {
      type: "choice",
      instructions: "Classify the excerpt's relevance to the question, based only on the supplied text.",
      criteria: {
        relevant: "Directly discusses refunds.",
        irrelevant: "Clearly does not discuss refunds.",
        unclear: "The supplied text is insufficient to decide."
      }
    }
  }
});
const answer = result.answers?.relevance;
if (result.stopReason !== "stop" || answer?.type !== "choice" ||
    !["relevant", "irrelevant", "unclear"].includes(answer.choice)) {
  return { status: "unavailable_or_invalid", error: result.errorMessage };
}
return { status: "ok", answer };
```

For tool discovery, `await searchTools(query, { limit: 8 })` yields candidate names and descriptions, including deferred tools. Compare relevant candidates if helpful; then use `await describeTool(name)` to inspect the selected operation and its parameters. For an MCP operation, also read and follow the server instructions from `describeNamespace("mcp__<server>")`; those instructions are not part of the tool description. An MCP call may resolve with `isError: true`, so check that flag before consuming its content, as well as handling thrown errors.

`getAvailableOfType()` reports models with available credentials, not guaranteed successful inference or permission to transmit the data. Filter candidates by the provider and data policy before choosing one; the example's first Jev match assumes all returned providers are permitted. `classify()` can return `stopReason: "error"` or `"aborted"` rather than throwing; discovery and invocation can also throw. Handle both forms of failure and retain a non-classifier path. Provider calls can incur cost and transmit supplied data.
