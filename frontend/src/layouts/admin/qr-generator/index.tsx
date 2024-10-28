import { QRCodeSVG } from "qrcode.react"
import * as React from "react"
import qrLogo from "./qr-logo.png"

type QRGeneratorProps = {
  domain: string,
  path: string,
  code: string,
}

const QRGenerator: React.FC<QRGeneratorProps> = ({ domain, path, code }) => {
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

export default QRGenerator
