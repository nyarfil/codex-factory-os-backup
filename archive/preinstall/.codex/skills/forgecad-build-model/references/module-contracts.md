# Module Contracts

Use this when planning or writing multi-file ForgeCAD models.

## Builder-First Modules

Reusable `.forge.js` files should return builder functions or module interfaces. Direct-run preview controls belong inside `if (require.main === module)`, like Python's `if __name__ == "__main__"`.

```js
function buildMount({ wall }) {
  const shape = box(80, 40, wall);
  return {
    shape,
    boltPattern: { diameter: 5.3, positions: [[-25, 0], [25, 0]] },
  };
}

if (require.main === module) {
  return buildMount({ wall: param('Wall', 3) }).shape;
}

return { buildMount };
```

The parent imports the module interface and passes ordinary values:

```js
const mountModule = require('./modules/mount/motor-mount.forge.js');
const mount = mountModule.buildMount({ wall });
```

## Assembly Contract

- Build each physical module in local coordinates around its own origin.
- Expose connectors and metadata as the module's public interface.
- Position structural members in parent modules through connectors, `connect()`, `match()`, or `matchTo()`.
- Route data through the parent: props flow down, computed metadata flows up. Siblings do not import each other.
- Use `verify.*` for interface claims. Do not use `console.log()` plus `if` as validation.

## Rejection Signals

- Shared dims/layout files that hand child modules assembly-space positions so they self-position.
- Pure `compute(params) -> D` dimension trees are not rejection signals when they are read-only data contracts.
- Sibling `require()` for placement data.
- Assembly-space coordinates inside a child module.
- Final `translate()` used to mate a structural part that should have a connector.
- Bare `connector.neutral()` outside a reusable component library with compatibility checks.
- A module whose direct-run preview returns something materially different from the builder contract imported by parents.

A shared dimension tree is allowed when it is pure data: it exports `compute(params)` or constants, returns plain JS numbers, arrays, and objects, imports no part modules, creates no ForgeCAD geometry, and has no side effects. Parts may consume it for local dimensions and local connector/interface coordinates. The parent may consume it for assembly-owned layout facts, scene dimensions, and connector seating. Parts still build at their own origin; the parent still positions physical modules through connectors.

Before advancing, ask:

1. Can the module be understood without reading sibling modules?
2. Can the module be previewed directly with `require.main === module`?
3. Does the parent compose modules through explicit interfaces rather than hidden coordinate math?
