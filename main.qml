import QtQuick 2.2

Rectangle {
    width: 800
    height: 700

    gradient: Gradient {
        GradientStop { position: 0.0; color: "#b0c5de" }
        GradientStop { position: 1.0; color: "slategray" }
    }

    ListModel {
        id: categoryListModel
        ListElement {
            name: "Ações"
            image:  "/Users/grey/Desktop/teste/imagCateg/ir.gif"
            color: "#41ae31"
            selected: false

            symbols: [
                ListElement {
                    name: "voltar"
                    image: "/Users/grey/Desktop/teste/seta.jpg"
                },
                ListElement {
                    name: "Beber"
                    image: "/Users/grey/Desktop/teste/simbolos/acoes/beber.jpg"
                },
                ListElement {
                    name: "Comer"
                    image: "/Users/grey/Desktop/teste/simbolos/acoes/comer.jpg"
                },
                ListElement {
                    name: "Ir"
                    image: "/Users/grey/Desktop/teste/simbolos/acoes/ir.jpg"
                },
                ListElement {
                    name: "Jogar"
                    image: "/Users/grey/Desktop/teste/simbolos/acoes/jogar.jpg"
                },
                ListElement {
                    name: "Tomar Banho"
                    image: "/Users/grey/Desktop/teste/simbolos/acoes/tomarBanho.jpg"
                }
            ]
        }

        ListElement {
            name:  "Comida"
            image:  "/Users/grey/Desktop/teste/imagCateg/comida.gif"
            color: "#e36123"
            selected: false

            symbols: [
                ListElement {
                    name: "Banana"
                    image: "/Users/grey/Desktop/teste/simbolos/comida/banana.jpg" },
                ListElement {
                    name: "Chocolate"
                    image: "/Users/grey/Desktop/teste/simbolos/comida/choco.jpg" },
                ListElement {
                    name: "Comida"
                    image: "/Users/grey/Desktop/teste/simbolos/comida/comida.jpg" },
                ListElement {
                    name: "Melancia"
                    image: "/Users/grey/Desktop/teste/simbolos/comida/melancia.jpg" }
            ]
        }

        ListElement {
            name: "Dias Da Semana"
            image:  "/Users/grey/Desktop/teste/imagCateg/week.png"
            color: "#fcef91"
            selected: false

            symbols: [
                ListElement {
                    name: "Segunda"
                    sText: "Segunda"
                    image: ""
                },
                ListElement {
                    itemName: "Terça"
                    sText: "Terça"
                    image: ""
                },
                ListElement {
                    itemName: "Quarta"
                    sText: "Quarta"
                    image: ""
                },
                ListElement {
                    itemName: "Quinta"
                    sText: "Quinta"
                    image: ""
                },
                ListElement {
                    itemName: "Sexta"
                    sText: "Sexta"
                    image: ""
                }
            ]
        }
    }

    property int currentCategory:   0
    property int currentSymbolIndex: 0
    property bool isInCategory:     false
    property bool selectedSymbol:   false

    property Column currentColumn;
    property ListView currentSymbols;
    property Rectangle currentSymbolRect;

    property int timerIntervalInSeconds: 2
    property int symbolCount: 0

    function performClick() {
        if (!isInCategory) {
            selectCategory(currentCategory);
        }
        else {
            var symbolInModel = categoryListModel.get(currentCategory).symbols.get(currentSymbolIndex).name;

            if (symbolInModel === "voltar") {
                isInCategory = false;
                categoryListModel.setProperty(currentCategory, "selected", false)
            }
            else {
                // TODO: Speak
                console.log(symbolInModel);
            }
        }
    }

    function tick() {
        if (selectedSymbol) {
        }
        else if (isInCategory) {
            currentSymbolIndex = (currentSymbolIndex + 1) % symbolCount;
            currentSymbols.currentIndex = currentSymbolIndex
        }
        else {
            currentCategory = (currentCategory + 1) % categoryListModel.count
            categoryList.currentIndex = currentCategory
        }
    }

    function selectCategory(index) {
        for (var i = 0; i < categoryListModel.count; i++)
            if (i !== index)
                categoryListModel.setProperty(i, "selected", false)

        categoryListModel.setProperty(index, "selected", true)
        for (var j = 0; j < currentColumn.children.length; j++)
            currentSymbols = currentColumn.children[j];

        // Colocando o numero de simbolos dessa categoria
        symbolCount = currentSymbols.count;
        console.log("Encontrados " + symbolCount + " simbolos");

        isInCategory = true;
    }

    Timer {
        interval: timerIntervalInSeconds * 1000;
        repeat: true;
        running: true;
        onTriggered: { tick(); }
    }

    Rectangle {
        x: 10
        y: 10
        width: 60
        height: 60
        border.color: "black"
        radius: 20

        gradient: Gradient {
            GradientStop { position: 0.0; color: "lightgreen" }
            GradientStop { position: 1.0; color: "darkgreen" }
        }

        Text {
            text: "CLICK"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                performClick()
            }
        }
    }

    Image {
        width: 120
        height: 60
        x: (parent.width - width)/2;
        y: 10
        source: "/Users/grey/Desktop/teste/dpcs.png"
    }

    ListView {
        id: categoryList
        x: 0
        spacing: 10
        anchors.fill: parent
        anchors.topMargin: 80
        model: categoryListModel

        highlight: Rectangle {
            height: 100
            width: 800
            color: "transparent"
            border.color: "red"
            border.width: 5
            z: 1
        }

        delegate: Column {
            width: 800
            y: 60

            Rectangle {
                color: color
                height: 80
                width: 800
                border.color: "white"
                radius: 5

                Image {
                    width: 80
                    height: 60
                    x: 10
                    anchors.verticalCenter: parent.verticalCenter
                    source: image
                }

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    x: 100
                    font.pixelSize: 24
                    text: name
                }

                Loader {
                   id: subItemLoader

                   visible: selected
                   property variant subItemModel : symbols
                   sourceComponent: selected ? subItemColumnDelegate : null
                   onStatusChanged: {
                       if (status == Loader.Ready)
                           item.model = subItemModel

                       currentColumn = item;
                   }
               }
            }
        }
    }

    Component {
        id: subItemColumnDelegate
        Column {
            id: subItemRow
            property alias model : subItemRepeater.model
            width: 750
            x: 200
            ListView {
                y: 5
                width: 750
                id: subItemRepeater
                orientation: ListView.Horizontal
                highlight: Rectangle {
                    width:  80
                    height: 70
                    color: "transparent"
                    border.color: "yellow"
                    border.width: 5
                    z: 1
                }

                delegate: Rectangle {
                    color: "#FFFFFF"
                    width: 80
                    height: 70

                    Image {
                        width: 80
                        height: 70
                        source: image
                    }
                }
            }
        }
    }

    Component.onCompleted: { tick(); }
}
