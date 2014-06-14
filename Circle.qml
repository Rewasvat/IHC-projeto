import QtQuick 2.2

Rectangle {
    id: root

    readonly property real radius_: width / 2
    property variant innerRect: inner
    property alias innerChildren: inner.children

    height: width
    radius: width * 0.5

    Rectangle {
        id: inner
        width: Math.sqrt(2) * root.radius
        height: width
        anchors.centerIn: root

        color: 'transparent'
    }
}
