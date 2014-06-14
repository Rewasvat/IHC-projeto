import QtQuick 2.2
import QtQuick.Layouts 1.1

Circle {
    id: delegateRoot

    width: 200
    color: PathView.isCurrentItem ? '#5F99D2BB' : 'transparent'
    border.color: '#000000'
    border.width: PathView.isCurrentItem ? 1 : 0

    innerChildren: [
        ColumnLayout {
            anchors.fill: parent
            Image {
                source: model.image
                fillMode: Image.PreserveAspectFit

                Layout.fillHeight: true
                Layout.fillWidth: true
            }

            Text {
                text: model.name
                color: 'white'
                font.pointSize: 16
                fontSizeMode: Text.HorizontalFit
                horizontalAlignment: Text.AlignHCenter
                style: Text.Outline
                styleColor: 'black'

                Layout.fillWidth: true
            }
        }
    ]
}
