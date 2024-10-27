import type { HeadFC, PageProps } from "gatsby"
import { QRCodeSVG } from "qrcode.react"
import * as React from "react"
import qrLogo from "./qr-logo.png"

const IndexPage: React.FC<PageProps> = ({ location }) => {
  const queryParams = new URLSearchParams(location.search)

  const domain = queryParams.get("domain") || location.origin
  const path = queryParams.get("path") || "/code?code="
  const code = queryParams.get("code") || ""

  const url = `${domain}${path}${code}`

  return <main className="w-screen h-screen content-center text-center">
    <div className="max-w-[600px] m-auto">
      <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-primary">
        QR Code Generator
      </h1>
      <QRCodeSVG
        className="w-full h-full p-4 mx-auto"
        size={600}
        marginSize={4}
        value={url}
        level="H"
        imageSettings={{
          src: qrLogo,
          height: 200,
          width: 200,
          excavate: true,
        }}
      />
      <p className="text-xs sm:text-base">
        {domain}{path}
      </p>
      <p className="text-xs sm:text-base">
        {code}
      </p>
    </div>
  </main>
}

export default IndexPage

export const Head: HeadFC = () => <title>QR Code Generator</title>
