import QtQuick 2.0

Rectangle {
    ListModel {
        id: testModel

        ListElement {
            name: 'Ações'; image: 'simbolos/acoes.jpg'

            symbols: [
                ListElement { name: 'Ações'; image: 'simbolos/acoes.jpg' },
                ListElement { name: 'Comida'; image: 'simbolos/comida.jpg' },
                ListElement { name: 'Dias da Semana'; image: 'simbolos/diasDaSemana.jpg' },
                ListElement { name: 'Expressões'; image: 'simbolos/expressoes.jpg' },
                ListElement { name: 'Lugares'; image: 'simbolos/lugares.jpg' },
                ListElement { name: 'Ações'; image: 'simbolos/acoes.jpg' },
                ListElement { name: 'Comida'; image: 'simbolos/comida.jpg' },
                ListElement { name: 'Dias da Semana'; image: 'simbolos/diasDaSemana.jpg' },
                ListElement { name: 'Expressões'; image: 'simbolos/expressoes.jpg'},
                ListElement { name: 'Lugares'; image: 'simbolos/lugares.jpg' }
            ]
        }

        ListElement { name: 'Comida'; image: 'simbolos/comida.jpg' }
        ListElement { name: 'Dias da Semana'; image: 'simbolos/diasDaSemana.jpg' }
        ListElement { name: 'Expressões'; image: 'simbolos/expressoes.jpg' }
        ListElement { name: 'Lugares'; image: 'simbolos/lugares.jpg' }
        ListElement { name: 'Ações'; image: 'simbolos/acoes.jpg' }
        ListElement { name: 'Comida'; image: 'simbolos/comida.jpg' }
        ListElement { name: 'Dias da Semana'; image: 'simbolos/diasDaSemana.jpg' }
        ListElement { name: 'Expressões'; image: 'simbolos/expressoes.jpg' }
        ListElement { name: 'Lugares'; image: 'simbolos/lugares.jpg' }
    }

    width: 1280
    height: 720

    CircularCategoryView {
        anchors.fill: parent
        model: testModel
    }
}
