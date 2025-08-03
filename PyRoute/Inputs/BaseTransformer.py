"""
Created on Nov 07, 2024

@author: CyberiaResurrection
"""
import re
from typing import Optional

from lark import Transformer, Token


class BaseTransformer(Transformer):

    strip_list = [
        'pbg',
        'nobles',
        'zone',
        'allegiance',
        'base',
        'residual'
    ]

    star_classes = ['Ia', 'Ib', 'II', 'III', 'IV', 'V', 'VI', 'D']
    zone_codes = 'ARUFGB- '
    zone_active = 'ARUFGB'

    def __init__(self, visit_tokens: bool = True, raw=None):
        super().__init__(visit_tokens)
        self.raw = raw.strip('\n')
        self.crankshaft = False

    def starline(self, args) -> list[list]:
        # These are the as-parsed values, and we're confirming the values as needed
        trade = args[2]
        extensions = args[3]
        nobles = args[4].children[0][0]
        base = args[4].children[1][0]
        zone = args[4].children[2][0]
        pbg = args[5][0][0]
        worlds = args[5][1][0] if 1 < len(args[5]) else Token('__ANON__11', ' ')
        allegiance = args[5][2][0] if 2 < len(args[5]) else Token('__ANON__12', ' ')

        tradelen = sum([len(item) for item in trade]) + len(trade) - 1
        # Square up overspilled trade codes
        if 16 < tradelen and 3 <= len(trade) and 1 == len(extensions) and '' == extensions[0].value.strip() and \
                '' == nobles.value and '' != base.value and '' == zone.value:
            move_fwd = 3 == len(base.value) and base.value.isdigit()  # Will base code still make sense as PBG?
            move_rev = 3 == len(allegiance.value)  # Will allegiance code still make sense as PBG?
            if move_fwd and not move_rev:
                last = trade[-1]
                mid = trade[-2]
                zone.value = base.value
                base.value = last
                nobles.value = mid
                trade = trade[:-2]
            elif (move_rev and not move_fwd) or (move_fwd and move_rev):
                pass

        if '*' != base.value and '' != base.value and 3 != len(extensions):
            if not self.crankshaft and zone.value.upper() not in self.zone_active:
                if '' == nobles.value:
                    nobles.value = base.value
                    base.value = zone.value
                elif '' == zone.value:  # if only 1 extension child?
                    zone.value = base.value
                    base.value = nobles.value
                    nobles.value = ''
        elif '*' != base.value and 3 == len(extensions) and '' == nobles.value and '' != base.value and \
                '' == zone.value and pbg.value == allegiance.value:
            nobles.value = base.value
            base.value = pbg.value
            zone.value = worlds.value
            pbg.value = allegiance.value
            worlds.value = ' '
            if 7 == len(args):
                allegiance.value = args[6][0].value
                args[6][0].value = ''
            else:
                allegiance.value = ''
        # If there's no residual argument
        if 8 == len(args) and 1 < len(args[7]):
            tailend = args[7][2][0].value
            lenlast = min(4, len(tailend))
            counter = 0
            while counter < lenlast and (tailend[counter].isalnum() or '-' == tailend[counter] or '?' == tailend[counter]):
                if counter < lenlast:
                    counter += 1
            if counter < min(4, lenlast):  # if the allegiance overspills, move the overspill into the residual
                overrun = tailend[counter:]
                tailend = tailend[:counter]
                args[7][2][0].value = tailend
                newbie = Token('__ANON_14', overrun)
                args.append([newbie])
        return args

    def position(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        return args

    def starname(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        return args

    def trade(self, args) -> list[str]:
        trimmed = []
        for item in args:
            rawval = BaseTransformer.boil_down_double_spaces(item.value.strip())
            trimmed.append(rawval)
        return trimmed

    def extensions(self, args) -> list[list]:
        if 1 == len(args):
            return args
        return args

    def nobles(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        if '' == args[0].value:
            args[0].value = '-'
        return args

    def base(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        if '' == args[0].value:
            args[0].value = '-'
        return args

    def zone(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        if '' == args[0].value:
            args[0].value = '-'
        return args

    def pbg(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        return args

    def worlds(self, args) -> list[list]:
        raw = args[0].value
        if 1 < len(raw):
            raw = raw.strip()
        args[0].value = raw
        return args

    def allegiance(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        return args

    def world_alg(self, args) -> list[list]:
        return args

    def residual(self, args) -> list[list]:
        args[0].value = args[0].value.strip()
        return args

    def starname_transform(self, starname: str) -> tuple[str, str]:
        bitz = [item for item in starname.split(' ') if 0 < len(item)]
        uwp = bitz[-1]
        bitz = bitz[:-1]
        return ' '.join(bitz), uwp

    def trade_transform(self, trade) -> str:
        codes = []

        for kid in trade:
            codes.append(kid)

        return ' '.join(codes)

    def extensions_transform(self, extensions) -> tuple[Optional[str], Optional[str], Optional[str]]:
        if 1 == len(extensions):  # Fallback no-extensions
            return None, None, None
        data = {'ix': '', 'ex': '', 'cx': ''}
        for kid in extensions:
            if isinstance(kid, Token):
                val = str(kid.type)
                data[val] = kid.value
            else:
                val = str(kid.data)
                data[val] = kid.children[0].value
            data[val] = self.boil_down_double_spaces(data[val])

        return data['ix'], data['ex'], data['cx']

    def world_alg_transform(self, world_alg) -> tuple[str, str, str]:
        if 1 == len(world_alg):
            return world_alg[0][0], world_alg[0][1], world_alg[0][2]
        if '' == world_alg[1][0].value.strip():
            world_alg[1][0].value = '0'
        return world_alg[0][0].value, world_alg[1][0].value, world_alg[2][0].value

    def transform(self, tree) -> list[Optional[str]]:
        self.crankshaft = '' == tree.children[4].children[0].children[0].value.strip() and '-' == tree.children[4].children[
            1].children[0].value and '' == tree.children[4].children[2].children[0].value.strip() and 1 == self.raw.count(' -')\
                          and 1 == self.raw.count('-   ')
        tree = self._preprocess_trade_and_extensions(tree)
        tree = self._preprocess_tree_suspect_empty_trade_code(tree)
        tree = self._transform_tree(tree)
        parsed = {'ix': None, 'ex': None, 'cx': None, 'residual': ''}

        parsed['position'] = tree[0][0].value
        parsed['name'], parsed['uwp'] = self.starname_transform(tree[1][0].value)
        parsed['trade'] = self.trade_transform(tree[2])
        parsed['ix'], parsed['ex'], parsed['cx'] = self.extensions_transform(tree[3])
        parsed['nobles'] = tree[4].children[0][0].value
        parsed['base'] = tree[4].children[1][0].value
        parsed['zone'] = tree[4].children[2][0].value
        parsed['pbg'], parsed['worlds'], parsed['allegiance'] = self.world_alg_transform(tree[5])
        if 7 == len(tree):
            parsed['residual'] = tree[6][0].value

        parsed = self._square_up_parsed(parsed)
        self.trim_raw_string(parsed)
        rawbitz = self._trim_raw_bitz(parsed)
        parsed = self._square_up_parsed_zero(rawbitz[0], parsed)
        # parsed = self._square_up_parsed_one(rawbitz[1], parsed)
        parsed = self._square_up_allegiance_overflow(parsed)

        no_extensions = parsed['ix'] is None and parsed['ex'] is None and parsed['cx'] is None
        ex_ix = parsed['ix'] if parsed['ix'] is not None else ' '
        ex_ix = self.boil_down_double_spaces(ex_ix)
        extensions = (ex_ix) + ' ' + \
                     (parsed['ex'] if parsed['ex'] is not None else ' ') + ' ' + \
                     (parsed['cx'] if parsed['cx'] is not None else ' ')

        spacer = ' ' if no_extensions else None
        if no_extensions:
            extensions = ''

        # Currently aiming to drop-in replace the starline regex output
        data = [parsed['position'], parsed['name'], parsed['uwp'], parsed['trade'], extensions, parsed['ix'], parsed['ex'], parsed['cx'], spacer, spacer, spacer, parsed['nobles'], parsed['base'], parsed['zone'].upper(), parsed['pbg'], parsed['worlds'], parsed['allegiance'], parsed['residual']]

        return data

    def _preprocess_trade_and_extensions(self, tree):
        trade = tree.children[2]
        extensions = tree.children[3]
        ix_reg = r'\{ *[+-]?[0-6] ?\}$'

        # If trade has importance-extension child, we need to fix it
        counter = -1
        ix_found = False
        for kid in trade.children:
            counter += 1
            ix_match = re.match(ix_reg, kid.value)
            if ix_match is not None:
                ix_found = True
                break

        if not ix_found:
            return tree

        bitz = trade.children[counter:]
        bitz[0].type = 'ix'
        if 1 < len(bitz):
            bitz[1].type = 'ex'
        if 2 < len(bitz):
            bitz[2].type = 'cx'
        trade.children = trade.children[:counter]
        extensions.children.extend(bitz)

        return tree

    def _is_noble(self, noble_string):
        noble = "BCcDEeFfGH"
        return all(char in noble for char in noble_string)

    def _is_zone(self, zone_string):
        if 1 != len(zone_string):
            return False
        from PyRoute.Inputs.ParseStarInput import ParseStarInput
        return zone_string[0] in ParseStarInput.valid_zone

    def _preprocess_tree_suspect_empty_trade_code(self, tree):
        if 1 != len(tree.children[2].children):
            return tree
        if 1 != len(tree.children[3].children):
            return tree
        if 5 < len(tree.children[2].children[0]):
            return tree
        if 5 != len(tree.children[3].children[0]):
            return tree
        all_noble = self._is_noble(tree.children[2].children[0])
        if not all_noble:
            return tree
        if self._is_zone(tree.children[4].children[2].children[0].value.strip()):
            return tree
        tree.children[4].children[2].children[0].value = tree.children[4].children[1].children[0].value
        tree.children[4].children[1].children[0].value = tree.children[4].children[0].children[0].value
        tree.children[4].children[0].children[0].value = tree.children[2].children[0].value
        tree.children[2].children[0].value = ""

        return tree

    @staticmethod
    def _calc_trade_overrun(children, raw):
        from PyRoute.Inputs.ParseStarInput import ParseStarInput
        trade_ext = ''
        overrun = 0
        # first check whether trade codes are straight up aligned
        for item in children:
            trade_ext += item.value + ' '
        if trade_ext in raw:
            return 0
        num_child = len(children) - 1
        gubbinz = [item.value for item in children]
        nobles = [item for item in gubbinz if ParseStarInput.can_be_nobles(item)]
        if 0 == len(nobles):
            return 0
        if 1 < len(gubbinz) and ParseStarInput.can_be_nobles(gubbinz[-2]) and ParseStarInput.can_be_base(gubbinz[-1]):
            return 2

        for k in range(num_child, 1, -1):
            trade_bar = " ".join(gubbinz[:k])
            if trade_bar in raw:
                overrun = len(children) - k
                for j in range(k, len(children)):
                    if not ParseStarInput.can_be_nobles(gubbinz[j]):
                        overrun -= 1
                return overrun
        trade_ext = ' '
        i = 0
        for item in children:  # Dig out the largest left-subset of trade children that are in the raw string
            trade_ext += item.value + ' '
            if trade_ext in raw:  # if it worked with one space appended, try a second space
                substr = False
                if i < num_child:
                    substr = children[i + 1].value.rfind(item.value) == (len(children[i + 1].value) - len(item.value))

                if not substr:
                    trade_ext += ' '
                    if trade_ext not in raw:  # if it didn't, drop the second space
                        trade_ext = trade_ext[:-1]
            else:  # if appending the space didn't work, try without it
                trade_ext = trade_ext[:-1]
            # after all that, if we've overrun (such as a nobles code getting transplanted), throw hands up and move on
            if trade_ext not in raw:
                overrun += 1
            i += 1
        return overrun

    def _square_up_parsed(self, parsed):
        if ' ' != parsed['nobles'] and 0 < len(parsed['nobles']) and '' == parsed['base'] and '' == parsed['zone'] and \
                3 == len(parsed['allegiance']) and parsed['allegiance'][0].isdigit():
            parsed['base'] = parsed['pbg']
            parsed['zone'] = parsed['worlds']
            parsed['pbg'] = parsed['allegiance']
            parsed['worlds'] = ' '
            parsed['allegiance'] = parsed['residual']
            parsed['residual'] = ''

        return parsed

    def trim_raw_string(self, tree) -> None:
        assert self.raw is not None, "Raw string not supplied before trimming"
        strip_list = ['position', 'name', 'uwp', 'trade', 'ix', 'ex', 'cx']

        for dataval in strip_list:
            if dataval not in tree:
                continue
            rawval = tree[dataval]
            if rawval is not None:
                if rawval.startswith('{ '):
                    oldlen = 0
                    while oldlen != len(self.raw):
                        oldlen = len(self.raw)
                        self.raw = self.raw.replace('{  ', '{ ')

                index = self.raw.find(rawval)
                self.raw = self.raw.replace(rawval, '', 1)
                if 0 < index:
                    self.raw = self.raw[index:]
                # special-case trade-code removal
                if 'trade' == dataval and -1 == index:
                    bitz = rawval.split()
                    for valbit in bitz:
                        index = self.raw.find(valbit)
                        self.raw = self.raw.replace(valbit, '', 1)
                        if 0 < index:
                            self.raw = self.raw[index:]

    def _square_up_parsed_zero(self, rawstring, parsed):
        from PyRoute.Inputs.ParseStarInput import ParseStarInput
        bitz = [item for item in rawstring.split(' ') if '' != item]
        if 3 == len(bitz) and bitz[0] == parsed['nobles'] and bitz[1] == parsed['base'] and bitz[2] == parsed['zone']:
            return parsed
        if 2 == len(bitz) and "" == parsed['zone']:
            if 2 < len(bitz[0]):  # bitz[0] can only possibly be nobles, so return
                return parsed
            if 1 < len(bitz[1]):  # if bitz[1] is more than one char, it can't be a trade zone, so return
                return parsed
            non_noble = [item for item in bitz[0] if item not in ParseStarInput.valid_nobles]
            if 0 < len(non_noble):  # If one or more chars in bitz[0] is not a valid noble call, then we have a base code and trade zone
                parsed['zone'] = parsed['base']
                parsed['base'] = parsed['nobles']
                parsed['nobles'] = ''
                return parsed
        if 3 == len(bitz):
            parsed['nobles'] = bitz[0]
            parsed['base'] = bitz[1]
            parsed['zone'] = bitz[2]
            return parsed
        if 2 == len(bitz) and '*' != parsed['base']:
            bit_one_zone_code = bitz[1].upper() in self.zone_codes
            # bit_zero_empty = '-' == bitz[0] or '' == bitz[0]
            bit_zero_forced_noble = bitz[0].isalpha() and not bitz[0].isupper()
            if 1 < len(bitz[1]) or not bit_one_zone_code:  # if second bit won't fit as a trade zone, then we have nobles and base
                parsed['nobles'] = bitz[0]
                parsed['base'] = bitz[1]
                parsed['zone'] = ''
                return parsed
            if bit_zero_forced_noble:  # if bitz[0] doesn't fit as a base code, have nobles and base
                parsed['nobles'] = bitz[0]
                parsed['base'] = bitz[1]
                parsed['zone'] = ''
                return parsed
            if not rawstring.endswith('   ') and 4 > len(bitz[0]):
                parsed['nobles'] = ''
                parsed['base'] = bitz[0]
                parsed['zone'] = bitz[1]
                return parsed
            if rawstring.startswith('   '):
                if 4 > len(bitz[0]):
                    parsed['nobles'] = ''
                    parsed['base'] = bitz[0]
                    parsed['zone'] = bitz[1]
                    return parsed
            else:
                parsed['nobles'] = bitz[0]
                parsed['base'] = bitz[1]
                parsed['zone'] = ''
        return parsed

    def _square_up_parsed_one(self, rawstring, parsed):
        rawtrim = rawstring.lstrip()
        rawbitz = rawtrim.split(' ')
        trimbitz = self._square_up_star_codes(rawbitz)
        if 3 < len(trimbitz):
            if trimbitz[0].isdigit():
                parsed['worlds'] = trimbitz[0]
                parsed['allegiance'] = trimbitz[1]
                parsed['residual'] = ' '.join(trimbitz[2:])
            else:
                parsed['worlds'] = ' '
                parsed['allegiance'] = trimbitz[0]
                parsed['residual'] = ' '.join(trimbitz[1:])
        elif 3 == len(trimbitz):
            if trimbitz[0].isdigit():
                parsed['worlds'] = trimbitz[0]
                parsed['allegiance'] = trimbitz[1]
                parsed['residual'] = trimbitz[2]
            else:
                parsed['worlds'] = ' '
                parsed['allegiance'] = trimbitz[0]
                parsed['residual'] = trimbitz[1] + ' ' + trimbitz[2]
        elif len(rawtrim) + 3 <= len(rawstring):  # We don't have three matches, need to figure out how they drop in
            alg = trimbitz[0]
            rawtrim = rawtrim.replace(alg, '', 1)

            if 2 == len(trimbitz):
                allegiance = trimbitz[1]
                rawtrim = rawtrim.replace(allegiance, '', 1)
                if alg.isdigit() and 5 > len(alg) and 1 < len(allegiance) and (not allegiance[0].islower()):  # if first trimbit fits in worlds field, stick it there
                    parsed['worlds'] = alg
                    parsed['allegiance'] = allegiance
                    parsed['residual'] = rawtrim.strip()
                else:
                    parsed['worlds'] = ' '
                    parsed['allegiance'] = alg
                    parsed['residual'] = allegiance

            elif 1 == len(alg):  # Allegiance codes can't be single-char, so we actually have a worlds field
                parsed['worlds'] = alg
                parsed['allegiance'] = rawtrim.strip()
            else:
                parsed['worlds'] = ' '
                parsed['allegiance'] = alg
                parsed['residual'] = rawtrim.strip()
        else:  # Assume worlds field is _not_ blank
            if ' ' == parsed['worlds'] and 2 == len(trimbitz):  # if worlds field has been _parsed_ as blank, need to move allegiance and residual up one
                parsed['worlds'] = trimbitz[0]
                parsed['allegiance'] = trimbitz[1]
                parsed['residual'] = ''

        if '' == parsed['allegiance'].strip() and '' != parsed['residual']:  # Allegiance _must_ be filled, residual is optional, so switch them back if they're transposed
            parsed['allegiance'] = parsed['residual']
            parsed['residual'] = ''

        return parsed

    def _square_up_star_codes(self, rawbitz):
        foobitz = [item for item in rawbitz if '' != item]
        trimbitz = []
        num_bitz = len(foobitz)
        for i in range(0, num_bitz):
            item = foobitz[i]
            if '' == item:
                continue
            if 0 < i < num_bitz - 1:
                next_item = foobitz[i + 1]
                if next_item in self.star_classes:
                    item += ' ' + next_item
                    foobitz[i + 1] = ''
            trimbitz.append(item)

        return trimbitz

    def _square_up_allegiance_overflow(self, parsed):
        alleg = parsed['allegiance']
        if '----' == alleg or '--' == alleg:
            return parsed

        if alleg.startswith('----') and 4 <= len(alleg):
            parsed['allegiance'] = '----'
            parsed['residual'] = alleg[4:] + parsed['residual']
        elif alleg.startswith('--') and 4 <= len(alleg):
            parsed['allegiance'] = '--'
            parsed['residual'] = alleg[2:] + ' ' + parsed['residual']
        else:
            counter = 0
            while counter < len(alleg) and (alleg[counter].isalnum() or '-' == alleg[counter] or '?' == alleg[counter]) and 4 > counter:
                counter += 1
            if counter < len(alleg):
                spacer = ' ' if parsed['residual'] != '' else ''
                parsed['allegiance'] = alleg[:counter]
                parsed['residual'] = alleg[counter:] + spacer + parsed['residual']
        return parsed

    def _trim_raw_bitz(self, parsed):
        pbg = ' ' + parsed['pbg'] + ' '
        rawbitz = self.raw.split(pbg)
        oldlen = len(rawbitz)
        if 1 == oldlen:
            rawbitz.append('')
        if 2 < oldlen:
            collide = self._check_raw_collision(parsed)
            first = pbg.join(rawbitz[:-1]) if not collide else pbg.join(rawbitz[:-2])
            second = rawbitz[-1] if not collide else pbg.join(rawbitz[-2:])
            repack = []
            repack.append(first)
            repack.append(second)
            rawbitz = repack
        rawbitz[0] += ' '
        rawbitz[1] = ' ' + rawbitz[1]

        return rawbitz

    def _check_raw_collision(self, parsed):
        if parsed['pbg'] == parsed['worlds']:
            return True
        if parsed['pbg'] == parsed['allegiance']:
            return True
        return parsed['pbg'] == parsed['residual']

    @staticmethod
    def boil_down_double_spaces(dubbel: str) -> str:
        return " ".join(dubbel.split())
