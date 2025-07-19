// fetcher.js
// Abstracted fetch function for API calls

/**
 * Fetches data from a given URL with search params.
 * @param {string} url - The base URL to fetch from.
 * @param {Object} urlParams - Key-value pairs for URL search params.
 * @returns {Promise<{response: any, error: undefined | object}>}
 */
async function fetcher(url, urlParams = {}) {
  try {
    const apiUrl = new URL(url, window.location.origin);
    Object.entries(urlParams).forEach(([key, value]) => {
      apiUrl.searchParams.set(key, value);
    });
    const res = await fetch(apiUrl);
    if (!res.ok) {
      return { response: undefined, error: { status: res.status, statusText: res.statusText } };
    }
    const data = await res.json();
    return { response: data, error: undefined };
  } catch (err) {
    return { response: undefined, error: err };
  }
}
