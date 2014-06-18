import QtQuick 2.2

CircularPathView {
    id: pathView

    property var previousCategories: []
    property var currentCategory
    property var nextCategory

    pathMargin: 100
    delegate: CircularViewItem {}

    preferredHighlightBegin: 0.0
    preferredHighlightEnd: 1.0

    highlightRangeMode: PathView.ApplyRange

    focus: true
    Keys.onLeftPressed: decrementCurrentIndex()
    Keys.onRightPressed: incrementCurrentIndex()
    Keys.onSpacePressed: nextCategory = selectedCategory()
    Keys.onBackPressed: exitCategory()

    NumberAnimation on opacity {
        id: fadeOut
        to: 0.0
        onStopped: pathView._updateModel()
    }

    NumberAnimation on opacity {
        id: fadeIn
        to: 1.0
    }

    function selectedCategory() {
        var model_ = model;
        var curIdx = currentIndex;
        return model_[curIdx];
    }

    function exitCategory() {
        nextCategory = 'exit';
    }

    onNextCategoryChanged: {
        if(nextCategory) {
            fadeIn.stop();
            fadeOut.start();
        }
    }

    function _updateModel() {
        if(nextCategory) {
            var category = nextCategory;
            if(category === 'exit')
                category =  previousCategories.pop();

            model = category.symbols || category;
            currentCategory = category;
            nextCategory = null;
        }

    }
}
