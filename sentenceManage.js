.pragma library

var Util = {
    contains: function (list, obj, comparator) {
        for (var i = 0; i < list.length; i++) {
            if (comparator) {
                if (comparator(list[i], obj)) {
                    return true;
                }
            }
            else if (list[i] === obj) {
                return true;
            }
        }
        return false;
    },
    forEach: function (v, fn) {
      for (var i = 0; i < v.length; i++) {
          fn(v[i], i);
      }
  }
};

var SDatabase = {
    id: 0,
    data: [],
    getId: function () {
        SDatabase.id += 1;
        return SDatabase.id;
    },
    insert: function (symbols) {
        var newSentence = {
            id: SDatabase.getId(),
            symbols: symbols || [],
            toString: function () {
            	var strBuilder = '';
            	Util.forEach(symbols, function (el, idx) {
            		console.log(el.name);
            		strBuilder += el.name + (idx === symbols.length - 1 ? '' :  ' ');
            	});
            	return strBuilder;
            }
        };
        SDatabase.data.push(newSentence);

        return newSentence;
    },
    select: function (sentenceId) {
        if (sentenceId) { // SELECT * FROM Sentences WHERE id = sentenceId
            for (var i = 0; i < SDatabase.data.length; i++) {
                if (sentenceId === SDatabase.data[i].id)
                    return SDatabase.data[i];
            }
        }
        else { // SELECT * FROM Sentences
            return SDatabase.data;
        }
    },
    update: function (sentenceId, symbols) {
        var sentenceIndex = -1;
        Util.forEach(SDatabase.data, function (el, idx) {
            if (el.id === sentenceId) {
                sentenceIndex = idx;
            }
        });

        if (sentenceIndex > -1) {
        	if (typeof(symbols.length) != 'undefined') {
        		Util.forEach(symbols, function (el, idx) {
        			SDatabase.data[sentenceIndex].symbols.push(el);
        		});
        	}
        	else {
        		SDatabase.data[sentenceIndex].symbols.push(symbols);
        	}
        }
    }
};

var SManager = {
    startNewSentence: false,
    append: function (symbol, sentenceId) {
        if (sentenceId) {
            var sentence = SDatabase.select(sentenceId);
            sentence.symbols.push(symbol);
            SDatabase.update(sentenceId, sentence.symbols);

            return sentence;
        }
        else if (SManager.startNewSentence) {
            var symbols = [];
            symbols.push(symbol);
            var inserted = SDatabase.insert(symbols);

            SManager.startNewSentence = false;

            return inserted;
        }
        else {
        	var currentSentence = SManager.getCurrentSentence();

        	if (currentSentence) {
        		SDatabase.update(currentSentence.id, symbol);
        		return currentSentence;
        	}
        	else {
	            var symbols = [];
	            symbols.push(symbol);
	            var inserted = SDatabase.insert(symbols);

	            return inserted;
	        }
        }
    },
    getCurrentSentence: function () {
        SDatabase.data.sort(function (a, b) {
            return b.id - a.id;
        });
        return SDatabase.data[0];
    },
    speakCurrentSentence: function (speakerObj) {
        SManager.speakSentence(speakerObj, SManager.getCurrentSentence().id);
        SManager.startNewSentence = true;
    },
    speakSentence: function (speakerObj, sentenceId) {
    	var sentence = SDatabase.select(sentenceId);
    	
        console.log('   Will talk for id: ' + sentenceId);
        console.log('       Symbol count: '  + sentence.symbols.length);

        for (var i = 0; i < sentence.symbols.length; i++) {
        	var el = sentence.symbols[i];
        	console.log('          Speaking ' + el.name + '...');
            speakerObj.speak(el.name, el.sText);

            // Thread.Sleep(5000);
            for (var j = 0; j < 999999999; j++) { }
        }
    },
    getText: function (symbols) {
    	var strBuilder = '';
    	Util.forEach(symbols, function (el, idx) {
    		console.log(el.name);
    		strBuilder += el.name + (idx === symbols.length - 1 ? '' :  ' ');
    	});
    	return strBuilder;
    }
};

