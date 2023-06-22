import argparse
import qrcode
from PIL import Image


def create_qr_code(with_content=None, include_ac_logo=True, logo_width=200):

    if include_ac_logo:
        logo_link = './assets/Logo.png'
        logo =  Image.open(logo_link)

        # adjust image size
        wpercent = (logo_width / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((logo_width, hsize), Image.BILINEAR)


    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # adding URL or text to QRcode
    QRcode.add_data(with_content)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = 'Grey'

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGBA')

    if include_ac_logo:
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)

        logo_centered = Image.new("RGBA", QRimg.size)
        logo_centered.paste(logo, pos)
        QRimg = Image.alpha_composite(QRimg, logo_centered)

    return QRimg


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, required=True)
    parser.add_argument('-o', type=str, required=True)
    parser.add_argument('-w', type=int, required=False, default=200)

    args = parser.parse_args()
    qr = create_qr_code(with_content=args.c, logo_width=args.w)
    qr.save(args.o)