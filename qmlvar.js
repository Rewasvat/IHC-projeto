var _privs = {}
var _selectedCategories = {}

function isSelected(catName) {
	return typeof(_selectedCategories[catName]) === 'undefined' ? false : _selectedCategories[catName];
}

function select(catName) {
	_selectedCategories[catName] = true;
}

function unselect(catName) {
	_selectedCategories[catName] = false;
}
 
function priv(key) {
    var h = key.toString()
    var o = _privs[key]
    if (!o) {
        o = {}
        _privs[key] = o
    }
    return o
}

function priv(key, value) {
    _privs[key] = value;
}