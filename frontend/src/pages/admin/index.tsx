import type { HeadFC, PageProps } from "gatsby"
import { QRCodeSVG } from "qrcode.react"
import * as React from "react"

const IndexPage: React.FC<PageProps> = ({ location }) => {
  const queryParams = new URLSearchParams(location.search)

  const domain = queryParams.get("domain") || location.origin
  const code = queryParams.get("code") || ""

  const url = `${domain}/code/${code}`

  return <main className="w-screen h-screen content-center text-center">
    <div className="max-w-[600px] m-auto">
      <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-primary">
        QR Code Generator
      </h1>
      <QRCodeSVG value={url} size={600} className="w-full h-full p-4 mx-auto" level="H" marginSize={4} />
      <p className="text-xs sm:text-base">
        {domain}
      </p>
      <p className="text-xs sm:text-base">
        {code}
      </p>
    </div>
  </main>
}

export default IndexPage

export const Head: HeadFC = () => <title>QR Code Generator</title>
