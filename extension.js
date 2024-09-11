const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.commentEmptyLine', function () {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selections = editor.selections;
            editor.edit(editBuilder => {
                selections.forEach(selection => {
                    const position = selection.active;
                    const lineText = editor.document.lineAt(position.line).text;
                    if (lineText.trim() === '') {
                        editBuilder.insert(position, '#/ ');
                    } else {
                        vscode.commands.executeCommand('editor.action.commentLine');
                    }
                });
            });
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
};
