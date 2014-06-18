import QtQuick 2.2

Circle {
    id: delegateRoot

    width: 200
    color: PathView.isCurrentItem ? ccolor : 'transparent'
    border.color: 'yellow'
    border.width: PathView.isCurrentItem ? 4 : 0

    innerChildren: [
        Column {
            anchors.fill: parent
            Image {
                source: image
                fillMode: Image.PreserveAspectFit

                anchors.fill: parent
            }

            Text {
                text: name
                color: 'white'
                font.pointSize: 16
                fontSizeMode: Text.HorizontalFit
                horizontalAlignment: Text.AlignHCenter
                style: Text.Outline
                styleColor: 'black'

                anchors.fill: parent
            }
        }
    ]
}
