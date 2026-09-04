#include <bts/blockchain/withdraw_types.hpp>
#include <bts/blockchain/types.hpp>

#include <fc/crypto/sha256.hpp>
#include <fc/crypto/ripemd160.hpp>
#include <fc/io/raw.hpp>
#include <fc/variant.hpp>

#include <iostream>
#include <iomanip>
#include <vector>

static void print_hex(const std::vector<char>& data)
{
    std::ios old_state(nullptr);
    old_state.copyfmt(std::cout);

    for (unsigned char c : data)
        std::cout << std::hex
                  << std::setw(2)
                  << std::setfill('0')
                  << static_cast<unsigned int>(c);

    std::cout << std::endl;
    std::cout.copyfmt(old_state);
}

int main()
{
    using namespace bts::blockchain;

    const fc::sha256 chain_id(
        "3a658e5846c3258dfbcfd4df712aa31c"
        "ff81b25b2800e213fbe64c05c134ec60"
    );

    fc::variant chain_variant(chain_id);

    const fc::ripemd160 legacy_chain_id =
        chain_variant.as<fc::ripemd160>();

    fc::ecc::private_key new_private =
        fc::ecc::private_key::regenerate(
            fc::sha256(
                "00000000000000000000000000000000"
                "00000000000000000000000000000002"
            )
        );

    public_key_type new_key(
        new_private.get_public_key()
    );

    fc::sha256::encoder enc;

    fc::raw::pack(
        enc,
        legacy_chain_id
    );

    fc::raw::pack(
        enc,
        new_key
    );

    const fc::sha256 digest = enc.result();

    withdraw_with_pts claim;
    claim.new_key = new_key;

    /*
     * Dummy 65-byte signature.
     * We are testing raw serialization here,
     * not cryptographic validity.
     */
    for (size_t i = 0; i < sizeof(claim.pts_signature.data); ++i)
        claim.pts_signature.data[i] =
            static_cast<unsigned char>(i);

    std::vector<char> packed =
        fc::raw::pack(claim);

    std::cout << "LEGACY CHAIN ID: "
              << legacy_chain_id.str()
              << std::endl;

    std::vector<char> packed_new_key =
        fc::raw::pack(new_key);

    std::cout << "NEW PUBLIC KEY RAW: ";
    print_hex(packed_new_key);

    std::cout << "CLAIM DIGEST: "
              << digest.str()
              << std::endl;

    std::cout << "PACKED SIZE: "
              << packed.size()
              << std::endl;

    std::cout << "PACKED HEX: ";
    print_hex(packed);

    return 0;
}
