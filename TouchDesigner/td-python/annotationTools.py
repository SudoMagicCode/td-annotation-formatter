import re
from html.parser import HTMLParser


class annotationFormatter:
    HEADING1 = 2
    HEADING2 = 1.75
    HEADING3 = 1.5
    HEADING4 = 1.25

    BULLET_SUBSTITUTION = '    • '
    BULLET_SYMBOLS = ['-', '*']

    def __init__(self, ownerOp) -> None:
        self.OwnerOp = ownerOp
        self.parser = HTMLParser()

        self._heading1 = ownerOp.par.Heading1
        self._heading2 = ownerOp.par.Heading2
        self._heading3 = ownerOp.par.Heading3
        self._heading4 = ownerOp.par.Heading3

    @property
    def Heading1(self) -> float:
        return self._heading1.eval()

    @property
    def Heading2(self) -> float:
        return self._heading2.eval()

    @property
    def Heading3(self) -> float:
        return self._heading3.eval()

    @property
    def Heading4(self) -> float:
        return self._heading4.eval()

    @property
    def Code_color(self) -> tuple:
        return (
            int(self.OwnerOp.par.Coder.eval() * 255),
            int(self.OwnerOp.par.Codeg.eval() * 255),
            int(self.OwnerOp.par.Codeb.eval() * 255)
        )

    def _format_text(self, text: str) -> str:
        output = []
        for eachLine in text.split('\n'):
            if '#' in eachLine:
                header_count = eachLine.count("#")
                header_text = ''
                match header_count:
                    case 1:
                        header_text = self._addHeading(self.Heading1, eachLine)

                    case 2:
                        header_text = self._addHeading(self.Heading2, eachLine)

                    case 3:
                        header_text = self._addHeading(self.Heading3, eachLine)

                    case 4:
                        header_text = self._addHeading(self.Heading4, eachLine)

                # this is a header line
                output.append(header_text)
            else:
                updated_text: str = eachLine

                # check each line has at least one symbol in it
                if len(eachLine) > 0:
                    # look for bullet replacement symbols
                    if eachLine[0] in annotationFormatter.BULLET_SYMBOLS:
                        # replace only the first instance of that symbol with the substitution character
                        updated_text = eachLine.replace(
                            eachLine[0], annotationFormatter.BULLET_SUBSTITUTION, 1)

                code_formatting = self._check_color(updated_text)
                output.append(code_formatting)

        return "\n".join(output)

    def FormatTextFromOp(self, tdOp) -> str:
        output = self._format_text(tdOp.text)
        return output

    def FormatText(self, rawText: str) -> str:
        output = self._format_text(rawText)
        return output

    def FormatTextFromDict(self, textDict: dict, subKey: str) -> str:
        output = self._format_text(textDict.get(subKey))
        return output

    def _check_color(self, text: str) -> str:
        newText = text.replace(
            '<code>', f'{{#color{(self.Code_color)}}}')
        resetText = newText.replace('</code>', '{#reset()}')
        return resetText

    def _addHeading(self, size: int, text: str) -> str:
        heading_text: str = re.sub('#', '', text).strip()
        return f'{{#scale({size});}}{heading_text}{{#reset()}}'
