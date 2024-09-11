const vscode = require('vscode');

export function activate(context) {
    vscode.workspace.getConfiguration('editor').update('tokenColorCustomizations', {
        "textMateRules": [
            {
                "scope": "comment.line.vodelog",
                "settings": {
                    "foreground": "#FF8800",
                    "fontStyle": "italic"
                }
            }
        ]
    }, vscode.ConfigurationTarget.Global);
}

 
function deactivate() {
    // delete "scope": "comment.line.vodelog"
    vscode.workspace.getConfiguration('editor').update('tokenColorCustomizations', {
        "textMateRules": []
    }, vscode.ConfigurationTarget.Global);
}

module.exports = {
    activate,
    deactivate
}
