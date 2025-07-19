// utils.js
// Utility functions for common DOM selector patterns with types

/**
 * Gets an element by ID.
 * @param {string} id - The element ID.
 * @returns {HTMLElement | null}
 */
function byId(id) {
  return document.getElementById(id);
}

/**
 * Clones a node deeply.
 * @param {Node} node - The node to clone.
 * @returns {Node}
 */
function clone(node) {
  return node.cloneNode(true);
}

/**
 * Queries all elements matching a selector within an optional parent.
 * @param {string} selector - The CSS selector.
 * @param {ParentNode | Document} [parent=document] - The parent node to query within.
 * @returns {NodeListOf<Element>}
 */
function all(selector, parent = document) {
  return parent.querySelectorAll(selector);
}

/**
 * Queries the first element matching a selector within an optional parent.
 * @param {string} selector - The CSS selector.
 * @param {ParentNode | Document} [parent=document] - The parent node to query within.
 * @returns {Element | null}
 */
function one(selector, parent = document) {
  return parent.querySelector(selector);
}
