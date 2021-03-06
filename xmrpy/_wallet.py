# Copyright 2021 Rashad Alston

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
# EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from urllib.parse import urlparse
from xmrpy.t import Dict, List, Optional, Any, TransferType
from xmrpy._http import HttpClient, Headers, RpcResponse
from xmrpy._config import Config, config
from xmrpy._logger import logger
from xmrpy._result import *


class Client:
    def __init__(self, conf: Optional[Config] = None, headers: Optional[Headers] = None):
        self._config = conf or config
        self._http = HttpClient(headers, timeout=int(self._config.HTTP_READ_TIMEOUT))
        self.url = urlparse("http://" + self._config.WALLET_RPC_ADDR + "/json_rpc")

    def auth(self):
        self._http.set_digest_auth(self._config.DIGEST_USER_NAME, self._config.DIGEST_USER_PASSWORD)
        return self

    async def get_balance(self, account_index: int = 0, address_indices: List[int] = [0]) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_balance",
                "params": {"account_index": account_index, "address_indices": address_indices},  # type: ignore
            },
            Result.GetBalance,
        )

    async def get_address_index(self, address: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "get_address_index", "params": {"address": address}},
            Result.GetAddressIndex,
        )

    async def create_address(self, account_index: int, label: Optional[str] = None) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "create_address",
                "params": {"account_index": account_index, "label": label},
            },
            Result.CreateAddress,
        )

    async def label_address(self, major_index: int, minor_index: int, label: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "label_address",
                "params": {
                    "index": {"major": major_index, "minor": minor_index},
                    "label": label,
                },
            },
            Result.LabelAddress,
        )

    async def validate_address(
        self,
        address: str,
        any_net_type: bool = False,
        allow_openalias: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "validate_address",
                "params": {
                    "address": address,
                    "any_net_type": any_net_type,
                    "allow_openalias": allow_openalias,
                },
            },
            Result.ValidateAddress,
        )

    async def get_accounts(self, tag: Optional[str] = None) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_accounts",
                "params": {
                    "tag": tag,
                },
            },
            Result.GetAccounts,
        )

    async def create_account(self, label: Optional[str] = None) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "create_account",
                "params": {
                    "label": label,
                },
            },
            Result.CreateAccount,
        )

    async def label_account(self, account_index: int, label: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "label_account",
                "params": {
                    "account_index": account_index,
                    "label": label,
                },
            },
            Result.LabelAccount,
        )

    async def tag_accounts(self, tag: str, accounts: List[int]) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "tag_accounts",
                "params": {"tags": tag, "accounts": accounts},
            },
            Result.TagAccounts,
        )

    async def get_account_tags(
        self,
    ) -> RpcResponse[Result]:
        return await self._send(
            (
                {
                    "method": "get_account_tags",
                    "params": "",
                }
            ),
            Result.GetAccountTags,
        )

    async def untag_accounts(self, accounts: List[int]) -> RpcResponse[Result]:
        return await self._send(
            {"method": "untag_accounts", "params": {"accounts": accounts}},
            Result.UntagAccounts,
        )

    async def set_account_tag_description(self, tag: str, description: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "set_account_tag_description",
                "params": {"tag": tag, "description": description},
            },
            Result.SetAccountTagDescription,
        )

    async def get_height(self) -> RpcResponse[Result]:
        return await self._send({"method": "get_height"}, Result.GetHeight)

    async def transfer(
        self,
        destinations: List[Dict[str, int]],
        account_index: int = 0,
        subaddr_indices: Optional[List[int]] = None,
        priority: int = 0,
        mixin: int = 0,
        ring_size: int = 7,
        unlock_time: int = 0,
        get_tx_key: bool = True,
        do_not_relay: bool = False,
        get_tx_hex: bool = False,
        get_tx_metadata: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "transfer",
                "params": {
                    "destinations": destinations,
                    "account_index": account_index,
                    "subaddr_indices": subaddr_indices,
                    "priority": priority,
                    "mixin": mixin,
                    "ring_size": ring_size,
                    "unlock_time": unlock_time,
                    "get_tx_key": get_tx_key,
                    "do_not_relay": do_not_relay,
                    "get_tx_hex": get_tx_hex,
                    "get_tx_metadata": get_tx_metadata,
                },
            },
            Result.Transfer,
        )

    async def transfer_split(
        self,
        destinations: List[Dict[str, int]],
        account_index: int = 0,
        subaddress_indices: List[int] = [],
        mixin: int = 0,
        ring_size: int = 7,
        unlock_time: int = 0,
        get_tx_keys: bool = True,
        priority: int = 0,
        do_not_relay: bool = False,
        get_tx_hex: bool = False,
        new_algorithm: bool = False,
        get_tx_metadata: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "transfer_split",
                "params": {
                    "destinations": destinations,
                    "account_index": account_index,
                    "subaddress_indices": subaddress_indices,
                    "priority": priority,
                    "mixin": mixin,
                    "ring_size": ring_size,
                    "unlock_time": unlock_time,
                    "get_tx_key": get_tx_keys,
                    "do_not_relay": do_not_relay,
                    "get_tx_hex": get_tx_hex,
                    "new_algorithm": new_algorithm,
                    "get_tx_metadata": get_tx_metadata,
                },
            },
            Result.TransferSplit,
        )

    async def sign_transfer(self, unsigned_txset: str, export_raw: bool = False) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "sign_transfer",
                "params": {
                    "unsigned_tx_set": unsigned_txset,
                    "export_raw": export_raw,
                },
            },
            Result.SignTransfer,
        )

    async def submit_transfer(self, tx_data_hex: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "submit_transfer",
                "params": {"tx_data_hex": tx_data_hex},
            },
            Result.SubmitTransfer,
        )

    async def sweep_dust(
        self,
        get_tx_keys: bool = True,
        do_not_relay: bool = False,
        get_tx_hex: bool = False,
        get_tx_metadata: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "sweep_dust",
                "params": {
                    "get_tx_keys": get_tx_keys,
                    "do_not_relay": do_not_relay,
                    "get_tx_hex": get_tx_hex,
                    "get_tx_metadata": get_tx_metadata,
                },
            },
            Result.SweepDust,
        )

    async def sweep_all(
        self,
        address: str,
        account_index: int,
        subaddr_indices: List[int] = [0],
        priority: int = 0,
        mixin: int = 0,
        ring_size: int = 7,
        unlock_time: int = 0,
        get_tx_keys: Optional[bool] = True,
        below_amount: Optional[int] = None,
        do_not_relay: bool = False,
        get_tx_hex: bool = False,
        get_tx_metadata: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "methods": "sweep_all",
                "params": {
                    "address": address,
                    "account_index": account_index,
                    "subaddr_indices": subaddr_indices,
                    "priority": priority,
                    "mixin": mixin,
                    "ring_size": ring_size,
                    "unlock_time": unlock_time,
                    "get_tx_keys": get_tx_keys,
                    "below_amount": below_amount,
                    "do_not_relay": do_not_relay,
                    "get_tx_hex": get_tx_hex,
                    "get_tx_metadata": get_tx_metadata,
                },
            },
            Result.SweepAll,
        )

    async def sweep_single(
        self,
        address: str,
        account_index: int,
        key_image: str,
        subaddr_indices: List[int] = [0],
        priority: int = 0,
        mixin: int = 0,
        ring_size: int = 7,
        unlock_time: int = 0,
        get_tx_keys: Optional[bool] = True,
        below_amount: Optional[int] = None,
        do_not_relay: bool = False,
        get_tx_hex: bool = False,
        get_tx_metadata: bool = False,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "methods": "sweep_all",
                "params": {
                    "address": address,
                    "account_index": account_index,
                    "subaddr_indices": subaddr_indices,
                    "priority": priority,
                    "mixin": mixin,
                    "ring_size": ring_size,
                    "key_image": key_image,
                    "unlock_time": unlock_time,
                    "get_tx_keys": get_tx_keys,
                    "below_amount": below_amount,
                    "do_not_relay": do_not_relay,
                    "get_tx_hex": get_tx_hex,
                    "get_tx_metadata": get_tx_metadata,
                },
            },
            Result.SweepAll,
        )

    async def relay_tx(self, tx_hex: str) -> RpcResponse[Result]:
        return await self._send({"method": "relay_tx", "params": {"hex": tx_hex}}, Result.RelayTx)

    async def store(self) -> RpcResponse[Result]:
        return await self._send({"method": "store"}, Result.Store)

    async def get_payments(self, payment_id: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "get_payments", "params": {"payment_id": payment_id}},
            Result.GetPayments,
        )

    async def get_bulk_payments(self, payment_ids: List[str], min_block_height: int) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_bulk_payments",
                "params": {
                    "payment_ids": payment_ids,
                    "min_block_height": min_block_height,
                },
            },
            Result.GetBulkPayments,
        )

    async def incoming_transfers(
        self,
        transfer_type: TransferType,
        account_index: int = 0,
        subaddr_indices: Optional[List[int]] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "incoming_transfers",
                "params": {
                    "transfer_type": transfer_type.value,
                    "account_index": account_index,
                    "subaddr_indices": subaddr_indices,
                },
            },
            Result.IncomingTransfers,
        )

    async def query_key(self, key_type: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "query_key", "params": {"key_type": key_type}},
            Result.QueryKey,
        )

    async def make_integrated_address(
        self,
        standard_address: Optional[str] = None,
        payment_id: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "make_integrated_address",
                "params": {
                    "standard_address": standard_address,
                    "payment_id": payment_id,
                },
            },
            Result.MakeIntegratedAddress,
        )

    async def split_integrated_address(self, integrated_address: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "split_integrated_address",
                "params": {"integrated_address": integrated_address},
            },
            Result.SplitIntegratedAddress,
        )

    async def stop_wallet(self) -> RpcResponse[Result]:
        return await self._send({"method": "stop_wallet"}, Result.StopWallet)

    async def rescan_blockchain(self) -> RpcResponse[Result]:
        return await self._send({"method": "rescan_blockchain"}, Result.RescanBlockchain)

    async def set_tx_notes(self, txids: List[str], notes: List[str]) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "set_tx_notes",
                "params": {"txids": txids, "notes": notes},
            },
            Result.SetTxNotes,
        )

    async def get_tx_notes(self, txids: List[str]) -> RpcResponse[Result]:
        return await self._send(
            {"method": "get_tx_notes", "params": {"txids": txids}},
            Result.GetTxNotes,
        )

    async def set_attribute(self, key: str, value: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "set_attribute", "params": {"key": key, "value": value}},
            Result.SetAttribute,
        )

    async def get_attribute(self, key: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "get_attribute", "params": {"key": key}},
            Result.GetAttribute,
        )

    async def get_tx_key(self, txid: str) -> RpcResponse[Result]:
        return await self._send({"method": "get_tx_key", "params": {"txid": txid}}, Result.GetTxKey)

    async def check_tx_key(self, txid: str, tx_key: str, address: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "check_tx_key",
                "params": {"txid": txid, "tx_key": tx_key, "address": address},
            },
            Result.CheckTxKey,
        )

    async def get_tx_proof(self, txid: str, address: str, message: Optional[str] = None) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_tx_proof",
                "params": {
                    "txid": txid,
                    "address": address,
                    "message": message,
                },
            },
            Result.GetTxProof,
        )

    async def check_tx_proof(
        self,
        txid: str,
        address: str,
        signature: str,
        message: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "check_tx_proof",
                "params": {
                    "txid": txid,
                    "address": address,
                    "message": message,
                    "signature": signature,
                },
            },
            Result.CheckTxProof,
        )

    async def get_spend_proof(self, txid: str, message: Optional[str] = None) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_spend_proof",
                "params": {"txid": txid, "message": message},
            },
            Result.GetSpendProof,
        )

    async def check_spend_proof(self, txid: str, signature: str, message: Optional[str]) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "check_spend_proof",
                "params": {
                    "txid": txid,
                    "signature": signature,
                    "message": message,
                },
            },
            Result.CheckSpendProof,
        )

    async def get_reserve_proof(
        self,
        all: bool,
        account_index: int,
        amount: int,
        message: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_reserve_proof",
                "params": {
                    "all": all,
                    "account_index": account_index,
                    "amount": amount,
                    "message": message,
                },
            },
            Result.GetReserveProof,
        )

    async def check_reserve_proof(
        self, address: str, signature: str, message: Optional[str] = None
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "check_reserve_proof",
                "params": {
                    "address": address,
                    "signature": signature,
                    "message": message,
                },
            },
            Result.CheckReserveProof,
        )

    async def get_transfers(self) -> RpcResponse[Result]:
        return await self._send({"method": "get_transfers"}, Result.GetTransfers)

    async def get_transfer_by_txid(self, txid: str, account_index: int) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "get_transfer_by_txid",
                "txid": txid,
                "account_index": account_index,
            },
            Result.GetTransferByTxId,
        )

    async def describe_transfer(self):
        raise NotImplementedError

    async def sign(self, data: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "sign", "params": {"data": data}},
            Result.Sign,
        )

    async def verify(self, data: str, address: str, signature: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "verify",
                "params": {
                    "data": data,
                    "address": address,
                    "signature": signature,
                },
            },
            Result.Verify,
        )

    async def export_outputs(self, all: bool = False) -> RpcResponse[Result]:
        return await self._send(
            {"method": "export_outputs", "params": {"all": all}},
            Result.ExportOutputs,
        )

    async def import_outputs(self, outputs_data_hex: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "import_outputs",
                "params": {"outputs_data_hex": outputs_data_hex},
            },
            Result.ImportOutputs,
        )

    async def export_key_images(self, all: bool = False) -> RpcResponse[Result]:
        return await self._send(
            {"method": "export_key_images", "params": {"all": all}},
            Result.ExportKeyImages,
        )

    async def import_key_images(self, signed_key_images: List[SignedKeyImage]) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "import_key_images",
                "params": {"signed_key_images": signed_key_images},
            },
            Result.ImportKeyImages,
        )

    async def make_uri(
        self,
        address: str,
        amount: Optional[int] = None,
        payment_id: Optional[str] = None,
        recipient_name: Optional[str] = None,
        tx_description: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "make_uri",
                "params": {
                    "address": address,
                    "amount": amount,
                    "payment_id": payment_id,
                    "recipient_name": recipient_name,
                    "tx_description": tx_description,
                },
            },
            Result.MakeUri,
        )

    async def parse_uri(self, uri: str) -> RpcResponse[Result]:
        return await self._send({"method": "parse_uri", "params": {"uri": uri}}, Result.ParseUri)

    async def get_address_book(self, entries: List[int]) -> RpcResponse[Result]:
        return await self._send(
            {"method": "get_address_book", "params": {"entries": entries}},
            Result.GetAddressBook,
        )

    async def add_address_book(
        self,
        address: str,
        payment_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "add_address_book",
                "params": {
                    "address": address,
                    "payment_id": payment_id,
                    "description": description,
                },
            },
            Result.AddAddressBook,
        )

    async def edit_address_book(
        self,
        index: int,
        set_address: bool,
        set_description: bool,
        set_payment_id: bool,
        address: Optional[str] = None,
        description: Optional[str] = None,
        payment_id: Optional[str] = None,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "edit_address_book",
                "params": {
                    "index": index,
                    "set_address": set_address,
                    "set_description": set_description,
                    "set_payment_id": set_payment_id,
                    "address": address,
                    "description": description,
                    "payment_id": payment_id,
                },
            },
            Result.EditAddressBook,
        )

    async def delete_address_book(self, index: int) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "delete_address_book",
                "params": {"index": index},
            },
            Result.DeleteAddressBook,
        )

    async def refresh(self, start_height: int) -> RpcResponse[Result]:
        return await self._send(
            {"method": "refresh", "params": {"start_height": start_height}},
            Result.Refresh,
        )

    async def auto_refresh(self, enable: bool = True) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "auto_refresh",
                "params": {"enable": enable},
            },
            Result.AutoRefresh,
        )

    async def rescan_spent(self) -> RpcResponse[Result]:
        return await self._send({"method": "rescan_spent"}, Result.RescanSpent)

    async def start_mining(
        self,
        threads_count: int,
        do_background_mining: bool,
        ignore_battery: bool,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "start_mining",
                "params": {
                    "threads_count": threads_count,
                    "do_background_mining": do_background_mining,
                    "ignore_battery": ignore_battery,
                },
            },
            Result.StartMining,
        )

    async def stop_mining(self) -> RpcResponse[Result]:
        return await self._send({"method": "stop_mining"}, Result.StopMining)

    async def get_languages(self) -> RpcResponse[Result]:
        return await self._send({"method": "get_languages"}, Result.GetLanguages)

    async def create_wallet(self, filename: str, password: str, language: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "create_wallet",
                "params": {
                    "filename": filename,
                    "password": password,
                    "language": language,
                },
            },
            Result.CreateWallet,
        )

    async def generate_from_keys(
        self,
        filename: str,
        address: str,
        viewkey: str,
        password: str,
        autosave_current: bool = True,
        spendkey: Optional[str] = None,
        restore_height: int = 0,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "generate_from_keys",
                "params": {
                    "filename": filename,
                    "address": address,
                    "viewkey": viewkey,
                    "password": password,
                    "autosave_current": autosave_current,
                    "spendkey": spendkey,
                    "restore_height": restore_height,
                },
            },
            Result.GenerateFromKeys,
        )

    async def open_wallet(self, filename: str, password: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "open_wallet",
                "params": {"filename": filename, "password": password},
            },
            Result.OpenWallet,
        )

    async def restore_deterministic_wallet(
        self,
        name: str,
        password: str,
        seed: str,
        restore_height: int = 0,
        language: Optional[str] = None,
        seed_offset: Optional[str] = None,
        autosave_current: bool = True,
    ) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "restore_deterministic_wallet",
                "params": {
                    "name": name,
                    "password": password,
                    "seed": seed,
                    "restore_height": restore_height,
                    "language": language,
                    "seed_offset": seed_offset,
                    "autosave_current": autosave_current,
                },
            },
            Result.RestoreDeterministicWallet,
        )

    async def close_wallet(self) -> RpcResponse[Result]:
        return await self._send({"method": "close_wallet"}, Result.CloseWallet)

    async def change_wallet_password(self, old_password: str, new_password: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "change_wallet_password",
                "params": {
                    "old_password": old_password,
                    "new_password": new_password,
                },
            },
            Result.ChangeWalletPassword,
        )

    async def is_multisig(self) -> RpcResponse[Result]:
        return await self._send({"method": "is_multisig"}, Result.IsMultisig)

    async def prepare_multisig(self) -> RpcResponse[Result]:
        return await self._send({"method": "prepare_multisig"}, Result.PrepareMultisig)

    async def make_multisig(self, multisig_info: List[str], threshold: int, password: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "make_multisig",
                "params": {
                    "multisig_info": multisig_info,
                    "threshold": threshold,
                    "password": password,
                },
            },
            Result.MakeMultisig,
        )

    async def export_multisig_info(self, info: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "export_multisig_info", "params": {"info": info}},
            Result.ExportMultisigInfo,
        )

    async def import_multisig_info(self, info: List[str]) -> RpcResponse[Result]:
        return await self._send(
            {"method": "import_multisig_info", "params": {"info": info}},
            Result.ImportMultisigInfo,
        )

    async def finalize_multisig(self, multisig_info: List[str], password: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "finalize_multisig",
                "params": {
                    "multisig_info": multisig_info,
                    "password": password,
                },
            },
            Result.FinalizeMultisig,
        )

    async def sign_multisig(self, tx_data_hex: str) -> RpcResponse[Result]:
        return await self._send(
            {"method": "sign_multisig", "params": {"tx_data_hex": tx_data_hex}},
            Result.SignMultisig,
        )

    async def submit_multisig(self, tx_data_hex: str) -> RpcResponse[Result]:
        return await self._send(
            {
                "method": "submit_multisig",
                "params": {"tx_data_hex": tx_data_hex},
            },
            Result.SubmitMultisig,
        )

    async def get_version(self) -> RpcResponse[Result]:
        return await self._send({"method": "get_version"}, Result.GetVersion)

    async def transfer_sign_submit(self, **kwargs):
        """
        Custom RPC method intended to simplify the steps of sending a transfer
        """
        destinations = kwargs.get("destinations")
        account_index = kwargs.get("account_index")
        subaddress_indices = kwargs.get("subaddress_indices")
        priority = kwargs.get("priority")
        mixin = kwargs.get("mixin")
        ring_size = kwargs.get("ring_size")
        unlock_time = kwargs.get("unlock_time")
        get_tx_key = kwargs.get("get_tx_key")
        do_not_relay = kwargs.get("do_not_relay")
        get_tx_hex = kwargs.get("get_tx_hex")
        get_tx_metadata = kwargs.get("get_tx_metadata")

        args = tuple(
            filter(
                None,
                (
                    destinations,
                    account_index,
                    subaddress_indices,
                    priority,
                    mixin,
                    ring_size,
                    unlock_time,
                    get_tx_key,
                    do_not_relay,
                    get_tx_hex,
                    get_tx_metadata,
                ),
            )
        )

        result = await self.transfer(*args)

        if result.is_err():
            logger.error(".transfer() failed with: %s (%s)", result.error.message, result.error.code)
            return result

        unsigned_txset = kwargs.get("unsigned_txset")
        export_raw = kwargs.get("export_raw")

        result = await self.sign_transfer(unsigned_txset, export_raw)

        if result.is_err():
            logger.error(".sign_transfer() failed with: %s (%s)", result.error.message, result.error.code)
            return result

        tx_data_hex = kwargs.get("tx_data_hex")
        result = await self.submit_transfer(tx_data_hex)

        if result.is_err():
            logger.error(".submit_transfer() failed with: %s (%s)", result.error.message, result.error.code)
            return result

        return result

    async def _send(self, args: Dict[str, Any], ResultClass: Result) -> RpcResponse[Result]:
        data = Client._attach_default_params(args)
        rpcmsg: RpcResponse[Result] = await self._http.post(self.url.geturl(), data=data, ResultClass=ResultClass.value)
        return rpcmsg

    @staticmethod
    def _attach_default_params(data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"id": "0", "jsonrpc": "2.0"}
        payload.update(data)
        return payload
