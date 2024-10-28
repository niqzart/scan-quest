const baseUrl = new URL("http://localhost:5000")

export type FetcherArgs = {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE",
  path: string,
  query?: { [key: string]: any },
  headers?: { [key: string]: string },
  json?: any,
}

export type FetcherReturn = {
  response: Response,
  json?: any
}

export default async function fetcher(
  {
    method = "GET",
    path,
    query = {},
    headers = {},
    json
  }: FetcherArgs
): Promise<FetcherReturn> {
  if (json !== undefined) {
    headers["Content-Type"] = "application/json"
  }

  const response = await fetch(
    new URL(path + "?" + new URLSearchParams(query), baseUrl),
    {
      method,
      headers,
      credentials: "include",
      body: JSON.stringify(json),
    }
  )

  if (response.headers.get("content-type") === "application/json") {
    return {
      response,
      json: await response.json()
    }
  }

  return { response }
}
