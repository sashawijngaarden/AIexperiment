// Initialize global variables 
var     lButtonsMT, timeEnter;
var     sNames  = '';
var     sDT     = '';
var     sCurrent = '';
var     sTypeReveal = 'row';

// When page is loaded
window.addEventListener('DOMContentLoaded', () => {

    // Activate all mousetracking buttons
    lButtonsMT = document.getElementsByClassName(sTypeReveal);
    for (let i=0; i<lButtonsMT.length; i++) {
        let elem = lButtonsMT[i];

        if (elem.id === 'row-decision' || elem.classList.contains('dec-row')) {
            continue;
        }

        CreateMT(elem, elem.id);
    }

    // Decision Buttons 
    lDecBtns = document.getElementsByClassName("dec-btn");
    for (let i=0; i<lDecBtns.length; i++) {
        let elem    = lDecBtns[i];
        // Get column name from ID
        let dec     = elem.id.split('-')[1];
        // Add on-click function 
        elem.addEventListener('click',()=>{
            document.getElementById('sDec').value = dec;
            document.getElementById('sNames').value = sNames;
            document.getElementById('sDT').value = sDT;
            endPage();
        })
        
    }
    // Begin timer
    timeEnter = new Date();
    setInterval(()=>{
        if (sCurrent!='') {
            let now = new Date();
            let dt = (now - timeEnter)/1000;
            document.getElementById('test-text').innerHTML = `${sCurrent}:${dt}`
        }
    },50)
});


// *********************************************************************
// Function Name:   updateMT
// Functionality:   
//                  Updates global vars and inputs with latest active AOI
//
// input:           object id
//
// returns:         void
// *********************************************************************

function updateMT() {
    // Store/update current time
    let now = new Date();
    let dt = now - timeEnter;
    timeEnter = now;
    // Save dwell time on AOI
    if (sDT.length>0) {
        sDT =  `${sDT},${dt}`;
        sNames = `${sNames},${sCurrent}`;
    } else {
        sDT = `${dt}`;
        sNames = `${sCurrent}`;
        // If first fixation, also record time to first fixation
        document.getElementById('time2first').value = timeEnter - dt - startTime;
    }
}

// *********************************************************************
// Function Name:   hideEverything
// Functionality:   
//                  Hides all the elements with the class name mt-tgt
//
// input:           object id
//
// returns:         void
// *********************************************************************


function hideEverything() {
    // get all elements to be hidden
    lTgt = document.getElementsByClassName('mt-tgt');
    // add hidden class
    for (let i=0;i<lTgt.length; i++) {
        lTgt[i].classList.add('hide');
    }

}

// *********************************************************************
// Function Name:   activateMT
// Functionality:   
//                  Activate the elements mt-tgt with class tgt
//
// input:           object id
//
// returns:         void
// *********************************************************************


function activateMT(tgt) {
    hideEverything();
    let lTgt = document.getElementsByClassName(`mt-tgt ${tgt}`);
    for (let i=0;i<lTgt.length; i++) {
        lTgt[i].classList.remove('hide');
    }
}

// *********************************************************************
// Function Name:   CreateMT
// Functionality:   
//                  Converts an html element into a mousetracking element
//
// input:           elem, object
//
// returns:         void
// *********************************************************************

function CreateMT(elem,tgt) {
    elem.addEventListener("mouseenter", ()=>{
        elem.classList.add('hover');
        timeEnter = new Date();
        sCurrent = elem.id;
        console.log('entering');
        activateMT(tgt);
    })
    elem.addEventListener("mouseleave", ()=>{
        elem.classList.remove('hover');
        sCurrent = elem.id;
        updateMT(elem.id);
        console.log('leaving')
        sCurrent = '';
        // hideEverything();
    })
}

// *********************************************************************
// Function Name:   endDecPage
// Functionality:   
//                  function for the decision button/key
//
// input:           dec, decision to be recorded in variable
//
// returns:         void
// *********************************************************************


function endDecPage(dec) {
    // Store all mousetracking variables + decision for the page
    document.getElementById('iDec').value = dec;
    document.getElementById('sNames').value = sNames;
    document.getElementById('sDT').value = sDT;
    endPage();
}
