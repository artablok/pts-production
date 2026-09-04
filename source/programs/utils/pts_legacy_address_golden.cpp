#include <bts/blockchain/pts_address.hpp>
#include <bts/blockchain/address.hpp>
#include <fc/crypto/elliptic.hpp>
#include <fc/variant.hpp>
#include <fc/exception/exception.hpp>
#include <iostream>

int main()
{
    try
    {
        // Synthetic private key scalar = 2.
        // Test-only key, never used on Production.
        fc::ecc::private_key key;
        fc::from_variant(
            fc::variant(
                "0000000000000000000000000000000000000000000000000000000000000002"
            ),
            key
        );

        const auto pub = key.get_public_key();

        std::cout
            << std::string(bts::blockchain::pts_address(pub, true, 56))
            << "\n"
            << std::string(bts::blockchain::pts_address(pub, false, 56))
            << "\n"
            << std::string(bts::blockchain::pts_address(pub, true, 0))
            << "\n"
            << std::string(bts::blockchain::pts_address(pub, false, 0))
            << "\n"
            << std::string(bts::blockchain::address(
                   bts::blockchain::pts_address(pub, true, 56)))
            << "\n"
            << std::string(bts::blockchain::address(
                   bts::blockchain::pts_address(pub, false, 56)))
            << "\n"
            << std::string(bts::blockchain::address(
                   bts::blockchain::pts_address(pub, true, 0)))
            << "\n"
            << std::string(bts::blockchain::address(
                   bts::blockchain::pts_address(pub, false, 0)))
            << "\n";

        return 0;
    }
    catch (const fc::exception& e)
    {
        std::cerr << e.to_detail_string() << "\n";
        return 1;
    }
}
