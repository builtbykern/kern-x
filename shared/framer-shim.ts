/**
 * Local shim so components typecheck and preview outside Framer.
 * In Framer, `framer` is provided by the runtime — replace imports accordingly.
 */

export enum ControlType {
  Boolean = "boolean",
  Number = "number",
  String = "string",
  Color = "color",
  Enum = "enum",
  Array = "array",
  Object = "object",
  Image = "image",
  ResponsiveImage = "responsiveimage",
  Font = "font",
  Transition = "transition",
  Link = "link",
}

export type PropertyControls = Record<string, unknown>

export function addPropertyControls(
  _component: unknown,
  _controls: PropertyControls
): void {
  // no-op outside Framer
}
