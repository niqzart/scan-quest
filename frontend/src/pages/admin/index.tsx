import QRGenerator from "@/layouts/admin/qr-generator"
import type { HeadFC, PageProps } from "gatsby"
import * as React from "react"

const IndexPage: React.FC<PageProps> = ({ location }) => {
  const queryParams = new URLSearchParams(location.search)

  return <QRGenerator
    domain={queryParams.get("domain") || location.origin}
    path={queryParams.get("path") || "/code?code="}
    code={queryParams.get("code") || ""}
  />
}

export default IndexPage

export const Head: HeadFC = () => <title>QR Code Generator</title>
